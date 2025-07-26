// Frontend/src/components/common/ErrorBoundary.jsx
// Manejo de errores para lazy loading y chunks
import React from 'react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { 
            hasError: false, 
            error: null,
            isChunkError: false 
        };
    }

    static getDerivedStateFromError(error) {
        const isChunkError = error.name === 'ChunkLoadError' || 
                           error.message.includes('Loading chunk');
        
        return { 
            hasError: true, 
            error,
            isChunkError 
        };
    }

    componentDidCatch(error, errorInfo) {
        console.error('Error boundary caught an error:', error, errorInfo);
        
        // Si es un error de chunk, intentar recargar después de un breve delay
        if (this.state.isChunkError) {
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        }
    }

    handleRetry = () => {
        this.setState({ hasError: false, error: null, isChunkError: false });
    };

    render() {
        if (this.state.hasError) {
            if (this.state.isChunkError) {
                return (
                    <div className="min-h-screen flex items-center justify-center bg-gray-50">
                        <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-6">
                            <div className="flex items-center justify-center w-12 h-12 mx-auto bg-yellow-100 rounded-full">
                                <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                                </svg>
                            </div>
                            <div className="mt-4 text-center">
                                <h3 className="text-lg font-medium text-gray-900">
                                    Actualizando aplicación...
                                </h3>
                                <p className="mt-2 text-sm text-gray-500">
                                    Se ha detectado una nueva versión. Recargando automáticamente...
                                </p>
                                <div className="mt-4 flex justify-center">
                                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }

            return (
                <div className="min-h-screen flex items-center justify-center bg-gray-50">
                    <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-6">
                        <div className="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full">
                            <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <div className="mt-4 text-center">
                            <h3 className="text-lg font-medium text-gray-900">
                                Algo salió mal
                            </h3>
                            <p className="mt-2 text-sm text-gray-500">
                                Ha ocurrido un error inesperado. Por favor, intenta nuevamente.
                            </p>
                            <button
                                onClick={this.handleRetry}
                                className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                            >
                                Intentar nuevamente
                            </button>
                        </div>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
