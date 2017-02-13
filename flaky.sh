#!/bin/bash

tests="
html/browsers/browsing-the-web/unloading-documents/001.html
html/browsers/offline/application-cache-api/api_update.html
html/browsers/offline/application-cache-api/api_update_error.html
html/semantics/document-metadata/styling/LinkStyle.html
web-animations/interfaces/Animation/oncancel.html
pointerevents/compat/pointerevent_touch-action_two-finger_interaction-manual.html
service-workers/service-worker/fetch-request-resources.https.html
service-workers/service-worker/request-end-to-end.https.html
web-animations/interfaces/Animation/cancel.html
web-animations/interfaces/Animation/playbackRate.html
fullscreen/api/document-exit-fullscreen-timing-manual.html
dom/nodes/Element-matches.html
html/browsers/history/the-location-interface/location-protocol-setter-non-broken.html
html/browsers/history/the-location-interface/reload_post_1.html
html/browsers/origin/cross-origin-objects/cross-origin-objects.html
html/syntax/parsing/template/creating-an-element-for-the-token/template-owner-document.html
html/webappapis/system-state-and-capabilities/the-navigator-object/NavigatorID.html
"

for t in $tests; do
	sed -i 's/doctype/DOCTyPe/gi' $t
done
