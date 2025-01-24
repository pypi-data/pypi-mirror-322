odoo.define("redner.report", function(require) {
    "use strict";

    var ActionManager = require('web.ActionManager');

    ActionManager.include({
        _executeReportAction: function(action, options) {
            // Redner reports
            if (action.report_type === "redner") {
                console.log(action.report_type)
                return this._triggerDownload(action, options, "redner");
            }
            return this._super.apply(this, arguments);
        },
        _makeReportUrls: function(action) {
            var reportUrls = this._super.apply(this, arguments);
            reportUrls.redner = "/report/redner/" + action.report_name;
            // We may have to build a query string with `action.data`. It's the place
            // were report's using a wizard to customize the output traditionally put
            // their options.
            if (
                _.isUndefined(action.data) ||
                _.isNull(action.data) ||
                (_.isObject(action.data) && _.isEmpty(action.data))
            ) {
                if (action.context.active_ids) {
                    var activeIDsPath = "/" + action.context.active_ids.join(",");
                    reportUrls.redner += activeIDsPath;
                }
            } else {
                var serializedOptionsPath =
                    "?options=" + encodeURIComponent(JSON.stringify(action.data));
                serializedOptionsPath +=
                    "&context=" + encodeURIComponent(JSON.stringify(action.context));
                reportUrls.redner += serializedOptionsPath;
            }
            return reportUrls;
        },
    });

});