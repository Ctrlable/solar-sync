from __future__ import annotations
import re
def _transform_readme_links(content):
	A=content;B={'#gear-configuration':'configuration.md','#memo-options':'configuration.md#all-options','#hammer_and_wrench-services':'services.md','#solar_syncapply':'services.md#solar_syncapply','#solar_syncset_manual_control':'services.md#solar_syncset_manual_control','#solar_syncchange_switch_settings':'services.md#solar_syncchange_switch_settings','#robot-automation-examples':'automation-examples.md','#sos-troubleshooting':'troubleshooting.md','#exclamation-common-problems--solutions':'troubleshooting.md#common-problems-solutions','#bar_chart-graphs':'advanced/brightness-modes.md#graphs','#bulb-features':'index.md#features','#control_knobs-regain-manual-control':'advanced/manual-control.md','#eyes-see-also':'see-also.md'}
	for(C,D)in B.items():A=A.replace(f"]({C})",f"]({D})")
	return re.sub('\\[\\[ToC\\]\\([^)]+\\)\\]','',A)