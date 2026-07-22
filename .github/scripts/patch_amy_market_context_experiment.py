from pathlib import Path
import re

path = Path('AMY_Market_Context_V4.pine')
text = path.read_text(encoding='utf-8')
original = text


def replace_once(old: str, new: str, name: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{name}: expected exactly 1 match, found {count}')
    text = text.replace(old, new, 1)

replace_once(
'''amyDashV2_dispMult = input.float(1.20, "Displacement Body Mult", minval=0.80, maxval=3.0, step=0.05, group=amyDashV2_group)
amyDashV2_minSweepTicks = input.int(1, "False Sweep Filter Ticks", minval=0, maxval=20, group=amyDashV2_group)''',
'''amyDashV2_dispMult = input.float(1.20, "Displacement Body Mult", minval=0.80, maxval=3.0, step=0.05, group=amyDashV2_group)
// EXPERIMENT HONESTY FILTERS: raw zones remain contextual, but only stronger formations are retained.
// These constants are intentionally locked until the 2020-2025 regression test is rerun.
amyExpV5_fvgBodyMult = 1.20
amyExpV5_fvgMinGapAtr = 0.15
amyExpV5_fvgMaxGapAtr = 0.75
amyExpV5_obBodyMult = 2.00
amyExpV5_obMinWidthAtr = 0.30
amyExpV5_obMaxWidthAtr = 1.50
amyExpV5_dolMaxDistanceAtr = 1.00
amyExpV5_retestRequired = true
amyDashV2_minSweepTicks = input.int(1, "False Sweep Filter Ticks", minval=0, maxval=20, group=amyDashV2_group)''',
'insert experiment constants')

replace_once(
'''    var int _bullFvgCreatedBar = na
    var int _bearFvgCreatedBar = na
    var int _bullObCreatedBar = na
    var int _bearObCreatedBar = na''',
'''    var int _bullFvgCreatedBar = na
    var int _bearFvgCreatedBar = na
    var int _bullObCreatedBar = na
    var int _bearObCreatedBar = na

    // Acceptance requires persistence. One close outside is not enough.
    var int _bullFvgOutsideCloses = 0
    var int _bearFvgOutsideCloses = 0
    var int _bullObOutsideCloses = 0
    var int _bearObOutsideCloses = 0''',
'insert acceptance counters')

old_dol = '''    if _canStartNewDol
        if _sslSweepNow and not _bslSweepNow and not na(_bsl)
            _lastSweepDir := 1
            _lastSweepBar := _bi
            _sweptPrice := _ssl
            _sweepExtreme := _l

            // FIX DOL: lock direction, target, start bar, and structural extreme.
            _dolDirLocked := 1
            _dolTargetLocked := _bsl
            _dolStartBar := _bi
            _sweepExtremeLocked := _l
            _dolState := 1

        else if _bslSweepNow and not _sslSweepNow and not na(_ssl)
            _lastSweepDir := -1
            _lastSweepBar := _bi
            _sweptPrice := _bsl
            _sweepExtreme := _h

            // FIX DOL: lock direction, target, start bar, and structural extreme.
            _dolDirLocked := -1
            _dolTargetLocked := _ssl
            _dolStartBar := _bi
            _sweepExtremeLocked := _h
            _dolState := 1'''
new_dol = '''    if _canStartNewDol
        if _sslSweepNow and not _bslSweepNow and not na(_bsl)
            // Every sweep remains observable, but a DOL target is created only after the honesty filter passes.
            _lastSweepDir := 1
            _lastSweepBar := _bi
            _sweptPrice := _ssl
            _sweepExtreme := _l
            _dolDistanceCandidate = math.abs(_bsl - _c)
            _dolQuality = _biasDir == 1 and _invalidStatus == 0 and not na(_atr) and _dolDistanceCandidate <= _atr * amyExpV5_dolMaxDistanceAtr

            if _dolQuality
                _dolDirLocked := 1
                _dolTargetLocked := _bsl
                _dolStartBar := _bi
                _sweepExtremeLocked := _l
                _dolState := 1
            else
                _dolState := 0
                _dolDirLocked := 0
                _dolStartBar := na
                _dolTargetLocked := na
                _sweepExtremeLocked := na

        else if _bslSweepNow and not _sslSweepNow and not na(_ssl)
            // Every sweep remains observable, but a DOL target is created only after the honesty filter passes.
            _lastSweepDir := -1
            _lastSweepBar := _bi
            _sweptPrice := _bsl
            _sweepExtreme := _h
            _dolDistanceCandidate = math.abs(_ssl - _c)
            _dolQuality = _biasDir == -1 and _invalidStatus == 0 and not na(_atr) and _dolDistanceCandidate <= _atr * amyExpV5_dolMaxDistanceAtr

            if _dolQuality
                _dolDirLocked := -1
                _dolTargetLocked := _ssl
                _dolStartBar := _bi
                _sweepExtremeLocked := _h
                _dolState := 1
            else
                _dolState := 0
                _dolDirLocked := 0
                _dolStartBar := na
                _dolTargetLocked := na
                _sweepExtremeLocked := na'''
replace_once(old_dol, new_dol, 'replace DOL start filter')

old_fvg_create = '''    // FVG creation
    _bullFvgNew = not na(high[3]) and low[1] > high[3]
    _bearFvgNew = not na(low[3]) and high[1] < low[3]

    if _bullFvgNew
        _bullFvgTop := low[1]
        _bullFvgBtm := high[3]
        _bullFvgStatus := 1
        _bullFvgCreatedBar := _bi

    if _bearFvgNew
        _bearFvgTop := low[3]
        _bearFvgBtm := high[1]
        _bearFvgStatus := 1
        _bearFvgCreatedBar := _bi'''
new_fvg_create = '''    // FVG creation — retain only displacement-backed gaps with realistic ATR width.
    _bullFvgRaw = not na(high[3]) and low[1] > high[3]
    _bearFvgRaw = not na(low[3]) and high[1] < low[3]
    _bullFvgGap = _bullFvgRaw ? low[1] - high[3] : na
    _bearFvgGap = _bearFvgRaw ? low[3] - high[1] : na
    _bullFvgGapAtr = not na(_bullFvgGap) and not na(_atr) ? _bullFvgGap / math.max(_atr, syminfo.mintick) : na
    _bearFvgGapAtr = not na(_bearFvgGap) and not na(_atr) ? _bearFvgGap / math.max(_atr, syminfo.mintick) : na
    _bullFvgNew = _bullFvgRaw and _c > _o and _body >= _meanBody * amyExpV5_fvgBodyMult and _bullFvgGapAtr >= amyExpV5_fvgMinGapAtr and _bullFvgGapAtr <= amyExpV5_fvgMaxGapAtr
    _bearFvgNew = _bearFvgRaw and _c < _o and _body >= _meanBody * amyExpV5_fvgBodyMult and _bearFvgGapAtr >= amyExpV5_fvgMinGapAtr and _bearFvgGapAtr <= amyExpV5_fvgMaxGapAtr

    if _bullFvgNew
        _bullFvgTop := low[1]
        _bullFvgBtm := high[3]
        _bullFvgStatus := 1
        _bullFvgCreatedBar := _bi
        _bullFvgOutsideCloses := 0

    if _bearFvgNew
        _bearFvgTop := low[3]
        _bearFvgBtm := high[1]
        _bearFvgStatus := 1
        _bearFvgCreatedBar := _bi
        _bearFvgOutsideCloses := 0'''
replace_once(old_fvg_create, new_fvg_create, 'replace FVG creation filter')

old_fvg_state = '''    // FIX POI: monotonic FVG state machine; first touch may go directly Fresh -> Mitigated.
    if _bullFvgCanTransition and not na(_bullFvgLow)
        if _c < _bullFvgLow
            _bullFvgStatus := 4
        else if _bullFvgStatus == 1
            if _bullFvgMitigated
                _bullFvgStatus := 3
            else if _bullFvgTouched
                _bullFvgStatus := 2
        else if _bullFvgStatus == 2 and _bullFvgMitigated
            _bullFvgStatus := 3

    if _bearFvgCanTransition and not na(_bearFvgHigh)
        if _c > _bearFvgHigh
            _bearFvgStatus := 4
        else if _bearFvgStatus == 1
            if _bearFvgMitigated
                _bearFvgStatus := 3
            else if _bearFvgTouched
                _bearFvgStatus := 2
        else if _bearFvgStatus == 2 and _bearFvgMitigated
            _bearFvgStatus := 3'''
new_fvg_state = '''    // HONESTY FIX: one close outside is only a warning. Acceptance requires two consecutive closed M15 candles.
    if _bullFvgCanTransition and not na(_bullFvgLow)
        if _c < _bullFvgLow
            _bullFvgOutsideCloses += 1
            if _bullFvgOutsideCloses >= 2
                _bullFvgStatus := 4
        else
            _bullFvgOutsideCloses := 0
            if _bullFvgStatus == 1
                if _bullFvgMitigated
                    _bullFvgStatus := 3
                else if _bullFvgTouched
                    _bullFvgStatus := 2
            else if _bullFvgStatus == 2 and _bullFvgMitigated
                _bullFvgStatus := 3

    if _bearFvgCanTransition and not na(_bearFvgHigh)
        if _c > _bearFvgHigh
            _bearFvgOutsideCloses += 1
            if _bearFvgOutsideCloses >= 2
                _bearFvgStatus := 4
        else
            _bearFvgOutsideCloses := 0
            if _bearFvgStatus == 1
                if _bearFvgMitigated
                    _bearFvgStatus := 3
                else if _bearFvgTouched
                    _bearFvgStatus := 2
            else if _bearFvgStatus == 2 and _bearFvgMitigated
                _bearFvgStatus := 3'''
replace_once(old_fvg_state, new_fvg_state, 'replace FVG acceptance state')

old_ob_create = '''    // OB creation retains the original candle-selection logic.
    _bullDisp = _c > _o and _body > _meanBody * _dispMult and _c > high[2]
    _bearDisp = _c < _o and _body > _meanBody * _dispMult and _c < low[2]

    if _bullDisp
        _bullObTop := close[2] < open[2] ? open[2] : open[1]
        _bullObBtm := close[2] < open[2] ? low[2] : low[1]
        _bullObStatus := 1
        // Created bar is the confirming displacement bar, regardless of [2] or [1] source candle.
        _bullObCreatedBar := _bi

    if _bearDisp
        _bearObTop := close[2] > open[2] ? high[2] : high[1]
        _bearObBtm := close[2] > open[2] ? open[2] : open[1]
        _bearObStatus := 1
        // Created bar is the confirming displacement bar, regardless of [2] or [1] source candle.
        _bearObCreatedBar := _bi'''
new_ob_create = '''    // OB creation — require a genuine opposite candle, stronger displacement, and controlled ATR width.
    _bullObTopCandidate = open[2]
    _bullObBtmCandidate = low[2]
    _bearObTopCandidate = high[2]
    _bearObBtmCandidate = open[2]
    _bullObWidthAtr = not na(_atr) ? math.abs(_bullObTopCandidate - _bullObBtmCandidate) / math.max(_atr, syminfo.mintick) : na
    _bearObWidthAtr = not na(_atr) ? math.abs(_bearObTopCandidate - _bearObBtmCandidate) / math.max(_atr, syminfo.mintick) : na
    _bullDisp = _c > _o and _body > _meanBody * math.max(_dispMult, amyExpV5_obBodyMult) and _c > high[2]
    _bearDisp = _c < _o and _body > _meanBody * math.max(_dispMult, amyExpV5_obBodyMult) and _c < low[2]
    _bullObNew = _bullDisp and close[2] < open[2] and _bullObWidthAtr >= amyExpV5_obMinWidthAtr and _bullObWidthAtr <= amyExpV5_obMaxWidthAtr
    _bearObNew = _bearDisp and close[2] > open[2] and _bearObWidthAtr >= amyExpV5_obMinWidthAtr and _bearObWidthAtr <= amyExpV5_obMaxWidthAtr

    if _bullObNew
        _bullObTop := _bullObTopCandidate
        _bullObBtm := _bullObBtmCandidate
        _bullObStatus := 1
        _bullObCreatedBar := _bi
        _bullObOutsideCloses := 0

    if _bearObNew
        _bearObTop := _bearObTopCandidate
        _bearObBtm := _bearObBtmCandidate
        _bearObStatus := 1
        _bearObCreatedBar := _bi
        _bearObOutsideCloses := 0'''
replace_once(old_ob_create, new_ob_create, 'replace OB creation filter')

old_ob_state = '''    // FIX POI: monotonic OB state machine; first touch may go directly Fresh -> Mitigated.
    if _bullObCanTransition and not na(_bullObLowRaw)
        if _c < _bullObLowRaw
            _bullObStatus := 4
        else if _bullObStatus == 1
            if _bullObMitigated
                _bullObStatus := 3
            else if _bullObTouched
                _bullObStatus := 2
        else if _bullObStatus == 2 and _bullObMitigated
            _bullObStatus := 3

    if _bearObCanTransition and not na(_bearObHighRaw)
        if _c > _bearObHighRaw
            _bearObStatus := 4
        else if _bearObStatus == 1
            if _bearObMitigated
                _bearObStatus := 3
            else if _bearObTouched
                _bearObStatus := 2
        else if _bearObStatus == 2 and _bearObMitigated
            _bearObStatus := 3'''
new_ob_state = '''    // HONESTY FIX: one close outside is only a warning. Acceptance requires two consecutive closed M15 candles.
    if _bullObCanTransition and not na(_bullObLowRaw)
        if _c < _bullObLowRaw
            _bullObOutsideCloses += 1
            if _bullObOutsideCloses >= 2
                _bullObStatus := 4
        else
            _bullObOutsideCloses := 0
            if _bullObStatus == 1
                if _bullObMitigated
                    _bullObStatus := 3
                else if _bullObTouched
                    _bullObStatus := 2
            else if _bullObStatus == 2 and _bullObMitigated
                _bullObStatus := 3

    if _bearObCanTransition and not na(_bearObHighRaw)
        if _c > _bearObHighRaw
            _bearObOutsideCloses += 1
            if _bearObOutsideCloses >= 2
                _bearObStatus := 4
        else
            _bearObOutsideCloses := 0
            if _bearObStatus == 1
                if _bearObMitigated
                    _bearObStatus := 3
                else if _bearObTouched
                    _bearObStatus := 2
            else if _bearObStatus == 2 and _bearObMitigated
                _bearObStatus := 3'''
replace_once(old_ob_state, new_ob_state, 'replace OB acceptance state')

replace_once(
'amyDashV2_dolStatusText = amyDashV2_dolStatus == 1 ? "Active" : amyDashV2_dolStatus == 2 ? "Reached" : amyDashV2_dolStatus == 3 ? "Invalid" : amyDashV2_dolStatus == 4 ? "Expired" : amyDashV2_dolStatus == 5 ? "Abandoned" : "Neutral"',
'amyDashV2_dolStatusText = amyDashV2_dolStatus == 1 ? "Qualified Active" : amyDashV2_dolStatus == 2 ? "Reached" : amyDashV2_dolStatus == 3 ? "Invalid" : amyDashV2_dolStatus == 4 ? "Expired" : amyDashV2_dolStatus == 5 ? "Abandoned" : "No Qualified DOL"',
'change DOL status wording')

replace_once(
'amyDashV2_poiStatusText = amyDashV2_poiStatus == 1 ? "Fresh" : amyDashV2_poiStatus == 2 ? "Active" : amyDashV2_poiStatus == 3 ? "Mitigated" : amyDashV2_poiStatus == 4 ? "Failed" : "None"',
'amyDashV2_poiStatusText = amyDashV2_poiStatus == 1 ? "Fresh • OBS" : amyDashV2_poiStatus == 2 ? "Touched • OBS" : amyDashV2_poiStatus == 3 ? "Mitigated • OBS" : amyDashV2_poiStatus == 4 ? "Accepted • 2x M15 Close" : "None"',
'change POI status wording')

replace_once(
'amyDashV2_reason := amyDashV2_join(amyDashV2_reason, amyDashV2_dolStatus == 1 ? amyDashV2_dolText + " raw " + amyDashV2_price(amyDashV2_dolTarget) : "")',
'amyDashV2_reason := amyDashV2_join(amyDashV2_reason, amyDashV2_dolStatus == 1 ? amyDashV2_dolText + " qualified " + amyDashV2_price(amyDashV2_dolTarget) : "")',
'change DOL reason wording')

replace_once(
'table.cell(amyDashV2_table, 0, 0, "AMY MARKET CONTEXT V4", text_color=color.white, bgcolor=amyDashV2_headBg, text_size=size.tiny)',
'table.cell(amyDashV2_table, 0, 0, "AMY CONTEXT EXPERIMENT", text_color=color.white, bgcolor=amyDashV2_headBg, text_size=size.tiny)',
'change dashboard heading')

replace_once(
'amyEntryV3_validatedTarget = amyDashV2_dolStatus == 1 and amyEntryV3_targetQualityLocked\namyEntryV3_validatedTargetEvent = amyEntryV2_dolActiveEvent and amyEntryV3_targetQualityAtStart',
'amyEntryV3_validatedTarget = not amyExpV5_retestRequired and amyDashV2_dolStatus == 1 and amyEntryV3_targetQualityLocked\namyEntryV3_validatedTargetEvent = not amyExpV5_retestRequired and amyEntryV2_dolActiveEvent and amyEntryV3_targetQualityAtStart',
'disable old validated DOL claim')

text, n = re.subn(r'(?m)^(amyContextV4_poiEvent\s*=\s*)', r'\1not amyExpV5_retestRequired and ', text, count=1)
if n != 1:
    raise RuntimeError(f'disable POI claim: expected 1 match, found {n}')
text, n = re.subn(r'(?m)^(amyContextV4_asiaEntryEvent\s*=\s*)', r'\1not amyExpV5_retestRequired and ', text, count=1)
if n != 1:
    raise RuntimeError(f'disable Asia Entry claim: expected 1 match, found {n}')

replace_once(
'_dashDolState = amyDashV2_dolStatus == 1 ? (amyEntryV3_validatedTarget ? "VALIDATED TARGET" : "OBSERVATION ONLY") : amyDashV2_dolStatusText',
'_dashDolState = amyDashV2_dolStatus == 1 ? (amyExpV5_retestRequired ? "QUALIFIED • RETEST REQUIRED" : amyEntryV3_validatedTarget ? "VALIDATED TARGET" : "OBSERVATION ONLY") : amyDashV2_dolStatusText',
'change final DOL dashboard state')

text = text.replace('//==================== AMY ASSISTANT V4 — VALIDATED CLAIMS + OBSERVATION ====================//',
                    '//==================== AMY ASSISTANT V4 — EXPERIMENTAL DEPENDENCY REVALIDATION ====================//', 1)

if text == original:
    raise RuntimeError('patch made no changes')
path.write_text(text, encoding='utf-8')
print('Patched AMY_Market_Context_V4.pine successfully')
