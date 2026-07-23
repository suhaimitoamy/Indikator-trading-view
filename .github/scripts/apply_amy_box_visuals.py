from pathlib import Path

path = Path("AMY_Market_Context_Final.pine")
text = path.read_text(encoding="utf-8")
text = text.replace(
    'indicator("AMY Market Context Final", overlay=true, max_labels_count=300, max_lines_count=300)',
    'indicator("AMY Market Context Final", overlay=true, max_labels_count=100, max_lines_count=100, max_boxes_count=300)'
)
start = text.index("// Visuals.")
end = text.index("// Compact multi-timeframe dashboard", start)
new_visuals = r'''// ============================================================================
// VISUALS — BOX-BASED CHART OBJECTS
// ============================================================================
fvgAcceptedEvent = (bullFvgStatus == 4 and bullFvgStatus[1] != 4) or (bearFvgStatus == 4 and bearFvgStatus[1] != 4)
obAcceptedEvent = (bullObStatus == 4 and bullObStatus[1] != 4) or (bearObStatus == 4 and bearObStatus[1] != 4)

statusText(_s) =>
    _s == 1 ? "Fresh" : _s == 2 ? "Touched" : _s == 3 ? "Mitigated" : _s == 4 ? "Accepted" : "None"

stateText(_s) =>
    _s == 1 ? "ACTIVE" : _s == 2 ? "REACHED" : _s == 3 ? "INVALID" : _s == 4 ? "TIMEOUT" : "IDLE"

amyUpdateZone(box _old, bool _enabled, bool _newZone, float _top, float _bottom, string _text, color _bg, color _border, color _textColor) =>
    box _result = _old
    if not _enabled or na(_top) or na(_bottom)
        if not na(_result)
            box.delete(_result)
        _result := na
    else if _newZone or na(_result)
        if not na(_result)
            box.delete(_result)
        _result := box.new(left=bar_index, top=_top, right=bar_index + 20, bottom=_bottom, bgcolor=_bg, border_color=_border, border_width=1, text=_text, text_color=_textColor, text_size=size.tiny)
    else
        box.set_right(_result, bar_index + 20)
        box.set_top(_result, _top)
        box.set_bottom(_result, _bottom)
        box.set_bgcolor(_result, _bg)
        box.set_border_color(_result, _border)
        box.set_text(_result, _text)
        box.set_text_color(_result, _textColor)
    _result

amyEventBox(box _old, float _top, float _bottom, string _text, color _bg, color _border, color _textColor) =>
    if not na(_old)
        box.delete(_old)
    box.new(left=bar_index, top=_top, right=bar_index + 5, bottom=_bottom, bgcolor=_bg, border_color=_border, border_width=1, text=_text, text_color=_textColor, text_size=size.tiny)

// Active chart zones. Only the latest zone of each type is kept to avoid clutter.
var box bullFvgBox = na
var box bearFvgBox = na
var box bullObBox = na
var box bearObBox = na
var box dolTargetBox = na
var box asiaEntryBox = na

bullFvgVisible = bullFvgStatus > 0 and bullFvgStatus < 4
bearFvgVisible = bearFvgStatus > 0 and bearFvgStatus < 4
bullObVisible = bullObStatus > 0 and bullObStatus < 4
bearObVisible = bearObStatus > 0 and bearObStatus < 4

bullFvgNewVisual = bullFvgVisible and (not bullFvgVisible[1] or bullFvgHigh != bullFvgHigh[1] or bullFvgLow != bullFvgLow[1])
bearFvgNewVisual = bearFvgVisible and (not bearFvgVisible[1] or bearFvgHigh != bearFvgHigh[1] or bearFvgLow != bearFvgLow[1])
bullObNewVisual = bullObVisible and (not bullObVisible[1] or bullObHigh != bullObHigh[1] or bullObLow != bullObLow[1])
bearObNewVisual = bearObVisible and (not bearObVisible[1] or bearObHigh != bearObHigh[1] or bearObLow != bearObLow[1])

bullFvgBox := amyUpdateZone(bullFvgBox, showZones and bullFvgVisible, bullFvgNewVisual, bullFvgHigh, bullFvgLow, "BULL FVG\n" + statusText(bullFvgStatus), color.new(color.lime, 86), color.new(color.lime, 10), color.white)
bearFvgBox := amyUpdateZone(bearFvgBox, showZones and bearFvgVisible, bearFvgNewVisual, bearFvgHigh, bearFvgLow, "BEAR FVG\n" + statusText(bearFvgStatus), color.new(color.red, 86), color.new(color.red, 10), color.white)
bullObBox := amyUpdateZone(bullObBox, showZones and bullObVisible, bullObNewVisual, bullObHigh, bullObLow, "BULL OB\n" + statusText(bullObStatus), color.new(color.blue, 86), color.new(color.blue, 10), color.white)
bearObBox := amyUpdateZone(bearObBox, showZones and bearObVisible, bearObNewVisual, bearObHigh, bearObLow, "BEAR OB\n" + statusText(bearObStatus), color.new(color.orange, 86), color.new(color.orange, 10), color.white)

_visualAtr = math.max(nz(atr5, syminfo.mintick * 100.0), syminfo.mintick * 10.0)
_dolPad = _visualAtr * 0.08
_asiaPad = _visualAtr * 0.10

dolTargetBox := amyUpdateZone(dolTargetBox, showZones and dolActive, dolEvent, dolLockedTarget + _dolPad, dolLockedTarget - _dolPad, "DOL TARGET\nMODERATE 75%", color.new(color.yellow, 78), color.new(color.yellow, 0), color.black)
asiaEntryBox := amyUpdateZone(asiaEntryBox, showZones and asiaActive, asiaEntryEvent, asiaEntry + _asiaPad, asiaEntry - _asiaPad, "ASIA ENTRY\nHIGH 84.62%", color.new(color.lime, 78), color.new(color.lime, 0), color.black)

// Latest event markers are rendered as compact boxes on the chart.
var box fvgAcceptMark = na
var box obAcceptMark = na
var box fvgRevisitMark = na
var box obRevisitMark = na
var box dolResultMark = na
var box asiaResultMark = na

_aboveTop = high + _visualAtr * 0.24
_aboveBottom = high + _visualAtr * 0.06
_belowTop = low - _visualAtr * 0.06
_belowBottom = low - _visualAtr * 0.24

if showMarkers and fvgAcceptedEvent
    fvgAcceptMark := amyEventBox(fvgAcceptMark, _aboveTop, _aboveBottom, "FVG ACCEPT", color.new(color.orange, 18), color.orange, color.white)

if showMarkers and obAcceptedEvent
    obAcceptMark := amyEventBox(obAcceptMark, _belowTop, _belowBottom, "OB ACCEPT", color.new(color.blue, 18), color.blue, color.white)

if showMarkers and fvgPoiEvent
    fvgRevisitMark := amyEventBox(fvgRevisitMark, _belowTop, _belowBottom, "FVG REVISIT\nHIGH", color.new(color.green, 15), color.green, color.white)
else if showMarkers and fvgPoiHitEvent
    fvgRevisitMark := amyEventBox(fvgRevisitMark, _aboveTop, _aboveBottom, "FVG HIT", color.new(color.green, 10), color.green, color.white)

if showMarkers and obPoiEvent
    obRevisitMark := amyEventBox(obRevisitMark, _belowTop, _belowBottom, "OB REVISIT\nMODERATE", color.new(color.aqua, 15), color.aqua, color.black)
else if showMarkers and obPoiHitEvent
    obRevisitMark := amyEventBox(obRevisitMark, _aboveTop, _aboveBottom, "OB HIT", color.new(color.aqua, 10), color.aqua, color.black)

if showMarkers and dolHitEvent
    dolResultMark := amyEventBox(dolResultMark, _aboveTop, _aboveBottom, "DOL HIT", color.new(color.yellow, 8), color.yellow, color.black)
else if showMarkers and dolInvalidEvent
    dolResultMark := amyEventBox(dolResultMark, _aboveTop, _aboveBottom, "DOL INVALID", color.new(color.red, 8), color.red, color.white)

if showMarkers and asiaTpEvent
    asiaResultMark := amyEventBox(asiaResultMark, _aboveTop, _aboveBottom, "ASIA TP", color.new(color.lime, 8), color.lime, color.black)
else if showMarkers and asiaSlEvent
    asiaResultMark := amyEventBox(asiaResultMark, _aboveTop, _aboveBottom, "ASIA SL", color.new(color.red, 8), color.red, color.white)

if not showMarkers
    if not na(fvgAcceptMark)
        box.delete(fvgAcceptMark)
        fvgAcceptMark := na
    if not na(obAcceptMark)
        box.delete(obAcceptMark)
        obAcceptMark := na
    if not na(fvgRevisitMark)
        box.delete(fvgRevisitMark)
        fvgRevisitMark := na
    if not na(obRevisitMark)
        box.delete(obRevisitMark)
        obRevisitMark := na
    if not na(dolResultMark)
        box.delete(dolResultMark)
        dolResultMark := na
    if not na(asiaResultMark)
        box.delete(asiaResultMark)
        asiaResultMark := na

'''
text = text[:start] + new_visuals + text[end:]
path.write_text(text, encoding="utf-8")
print("AMY final visuals converted to boxes")
