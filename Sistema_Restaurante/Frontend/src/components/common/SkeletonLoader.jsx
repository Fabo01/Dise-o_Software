// Frontend/src/components/common/SkeletonLoader.jsx
// Implementa tarea S3-28: Añadir skeleton loaders
import React from 'react';

export const SkeletonCard = () => (
    <div className="animate-pulse bg-white shadow rounded-lg p-6">
        <div className="flex items-center space-x-4">
            <div className="rounded-full bg-gray-300 h-10 w-10"></div>
            <div className="flex-1 space-y-2">
                <div className="h-4 bg-gray-300 rounded w-3/4"></div>
                <div className="h-3 bg-gray-300 rounded w-1/2"></div>
            </div>
        </div>
        <div className="mt-4 space-y-3">
            <div className="h-3 bg-gray-300 rounded"></div>
            <div className="h-3 bg-gray-300 rounded w-5/6"></div>
        </div>
    </div>
);

export const SkeletonTable = ({ rows = 5, columns = 4 }) => (
    <div className="animate-pulse">
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <div className="px-4 py-5 sm:px-6">
                <div className="h-6 bg-gray-300 rounded w-1/4"></div>
            </div>
            <div className="border-t border-gray-200">
                {Array(rows).fill(0).map((_, rowIndex) => (
                    <div key={rowIndex} className="px-4 py-4 border-b border-gray-200 flex space-x-4">
                        {Array(columns).fill(0).map((_, colIndex) => (
                            <div key={colIndex} className="flex-1">
                                <div className="h-4 bg-gray-300 rounded"></div>
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    </div>
);

export const SkeletonChart = () => (
    <div className="animate-pulse bg-white p-6 rounded-lg shadow">
        <div className="mb-4">
            <div className="h-6 bg-gray-300 rounded w-1/3"></div>
        </div>
        <div className="h-64 bg-gray-200 rounded"></div>
    </div>
);

export const SkeletonList = ({ items = 3 }) => (
    <div className="animate-pulse">
        {Array(items).fill(0).map((_, index) => (
            <div key={index} className="border-b border-gray-200 py-4">
                <div className="flex items-center space-x-3">
                    <div className="h-8 w-8 bg-gray-300 rounded-full"></div>
                    <div className="flex-1 space-y-2">
                        <div className="h-4 bg-gray-300 rounded w-3/4"></div>
                        <div className="h-3 bg-gray-300 rounded w-1/2"></div>
                    </div>
                    <div className="h-8 w-20 bg-gray-300 rounded"></div>
                </div>
            </div>
        ))}
    </div>
);

export const SkeletonForm = () => (
    <div className="animate-pulse space-y-6">
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
                <div className="h-4 bg-gray-300 rounded w-1/4 mb-2"></div>
                <div className="h-10 bg-gray-300 rounded"></div>
            </div>
            <div>
                <div className="h-4 bg-gray-300 rounded w-1/4 mb-2"></div>
                <div className="h-10 bg-gray-300 rounded"></div>
            </div>
        </div>
        <div>
            <div className="h-4 bg-gray-300 rounded w-1/4 mb-2"></div>
            <div className="h-24 bg-gray-300 rounded"></div>
        </div>
        <div className="flex justify-end space-x-3">
            <div className="h-10 w-20 bg-gray-300 rounded"></div>
            <div className="h-10 w-20 bg-gray-300 rounded"></div>
        </div>
    </div>
);

export const SkeletonDashboard = () => (
    <div className="animate-pulse">
        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {Array(4).fill(0).map((_, index) => (
                <div key={index} className="bg-white p-6 rounded-lg shadow">
                    <div className="flex items-center">
                        <div className="h-8 w-8 bg-gray-300 rounded-full mr-3"></div>
                        <div className="flex-1">
                            <div className="h-4 bg-gray-300 rounded w-3/4 mb-2"></div>
                            <div className="h-6 bg-gray-300 rounded w-1/2"></div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
        
        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <SkeletonChart />
            <SkeletonChart />
        </div>
    </div>
);

const SkeletonLoader = {
    Card: SkeletonCard,
    Table: SkeletonTable,
    Chart: SkeletonChart,
    List: SkeletonList,
    Form: SkeletonForm,
    Dashboard: SkeletonDashboard
};

export default SkeletonLoader;
