import React from 'react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = {hasError: false, error : null};
    }

    static getDerivedStateFromError(error) {
        return {hasError: true, error};
    }

    componentDidCatch(error, errorInfo) {
        console.error('ErrorBoundary caught and error:', error, errorInfo);
    }

    render() {
        if(this.state.hasError) {
            return(
            <div className="min-h-screen flex items-center justify-center bg-gray-50">
                <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-6 text-center">
                    <div className="text-6xl mb-4">😞</div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    Oups ! Une erreur est survenue
                    </h2>
                    <p className="text-gray-600 mb-6">
                    Nous nous excusons pour ce problème. Veuillez rafraîchir la page ou réessayer plus tard.
                    </p>
                    <button
                    onClick={() => window.location.reload()}
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                    🔄 Rafraîchir la page
                    </button>
                </div>
            </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;