// Frontend/src/hooks/usePagination.js
// Implementa tarea S3-27: Implementar paginación en listas
import { useState, useMemo } from 'react';

const usePagination = (data, itemsPerPage = 10) => {
    const [currentPage, setCurrentPage] = useState(1);
    
    const paginatedData = useMemo(() => {
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        return data.slice(startIndex, endIndex);
    }, [data, currentPage, itemsPerPage]);
    
    const totalPages = Math.ceil(data.length / itemsPerPage);
    const totalItems = data.length;
    
    const goToPage = (page) => {
        setCurrentPage(Math.max(1, Math.min(page, totalPages)));
    };
    
    const goToNextPage = () => {
        setCurrentPage(prev => Math.min(prev + 1, totalPages));
    };
    
    const goToPreviousPage = () => {
        setCurrentPage(prev => Math.max(prev - 1, 1));
    };
    
    const getPageNumbers = () => {
        const delta = 2;
        const range = [];
        const rangeWithDots = [];
        
        for (let i = Math.max(2, currentPage - delta);
             i <= Math.min(totalPages - 1, currentPage + delta);
             i++) {
            range.push(i);
        }
        
        if (currentPage - delta > 2) {
            rangeWithDots.push(1, '...');
        } else {
            rangeWithDots.push(1);
        }
        
        rangeWithDots.push(...range);
        
        if (currentPage + delta < totalPages - 1) {
            rangeWithDots.push('...', totalPages);
        } else {
            if (totalPages > 1) {
                rangeWithDots.push(totalPages);
            }
        }
        
        return rangeWithDots;
    };
    
    return {
        currentPage,
        totalPages,
        totalItems,
        paginatedData,
        goToPage,
        goToNextPage,
        goToPreviousPage,
        getPageNumbers,
        hasNextPage: currentPage < totalPages,
        hasPreviousPage: currentPage > 1,
        isFirstPage: currentPage === 1,
        isLastPage: currentPage === totalPages
    };
};

export default usePagination;
