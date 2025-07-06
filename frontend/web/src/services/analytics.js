class AnalyticsService {
    constructor() {
        this.GA_MEASUREMENT_ID = 'G-79VSBHWD02';
        this.isEnabled = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';

        if (this.isEnabled) {
            console.log('Google Analytics is enabled');
        }
        else {
            console.log('Google Analytics is disabled');
        }
    }

    trackAnalysisStart(filename = '', filesize = '') {
        this.trackEvent('analysis_started', {
            file_name: filename,
            file_size: filesize,
            timestamp: new Date().toISOString()
        });
    }

    trackAnalysisComplete(filename = '', analysisTime = 0) {
        this.trackEvent('analysis_completed', {
            file_name: filename,
            analysis_duration_seconds: analysisTime,
            timestamp: new Date().toISOString()
        });
    }

    trackReportExport(exportType = 'pdf') {
        this.trackEvent('report_exported', {
            export_type: exportType, // 'pdf' or 'print'
            page: window.location.pathname,
            timestamp: new Date().toISOString()
            });
    }

    trackTimeOnAnalysisPage(timeSpent) {
        this.trackEvent('time_on_analysis_page',{
            time_spent_seconds: Math.round(timeSpent),
            time_spent_minutes: Math.round(timeSpent / 60 * 10) / 10
        });
    }

    trackPageView(pageName) {
            this.trackEvent('page_view', {
                page_name: pageName,
                page_path: window.location.pathname,
                timestamp: new Date().toISOString()
            });
    }
    
    trackEvent(eventName, parameters = {}) {
        if ( !this.isEnabled) {
            console.log(`Dev event : ${eventName}`, parameters);
            return;;
        }

        try {
            if (typeof gtag !== 'undefined') {
                gtag('event', eventName, {
                    custom_parameter_1: parameters,
                    ...parameters
                });
                console.log(`Event tracked: ${eventName}`, parameters);
            }
        } catch(error) {
            console.error('Analytics error:', error);
        }
    }
}

export default new AnalyticsService();