'use client';

/**
 * useDataList - Generic hook for managing data list state with React Query
 * Handles fetching, pagination, filters, and WebSocket sync
 */

import React, { useEffect, useMemo, useState, useCallback } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';

interface UseDataListOptions<T> {
  fetchFn: (
    filters: Record<string, any>,
    pagination: { page: number; page_size: number }
  ) => Promise<{ items: T[]; total: number }>;
  wsItems: T[];
  setWsItems: (items: T[]) => void;
  token: string | null;
  initialFilters?: Record<string, any>;
  initialPage?: number;
  initialPageSize?: number;
  queryKey: string[]; // Unique key for React Query cache
}

export function useDataList<T>({
  fetchFn,
  wsItems,
  setWsItems,
  token,
  initialFilters = {},
  initialPage = 1,
  initialPageSize = 20,
  queryKey,
}: UseDataListOptions<T>) {
  const queryClient = useQueryClient();

  // Manage filters and pagination state
  const [filters, setFiltersState] = useState<Record<string, any>>({
    ...initialFilters,
    page: initialPage,
    page_size: initialPageSize,
  });

  // Extract pagination from filters
  const page = filters.page || initialPage;
  const page_size = filters.page_size || initialPageSize;
  const { page: _, page_size: __, ...apiFilters } = filters;

  // Create query key with filters and pagination
  const fullQueryKey = useMemo(
    () => [...queryKey, apiFilters, page, page_size],
    [queryKey, apiFilters, page, page_size]
  );

  // Track if this is the initial mount to prevent hydration mismatch
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Use React Query for data fetching
  const {
    data: queryData,
    isLoading,
    isPending,
    error: queryError,
    refetch,
  } = useQuery({
    queryKey: fullQueryKey,
    queryFn: async () => {
      if (!token) {
        return { items: [], total: 0 };
      }
      return await fetchFn(apiFilters, { page, page_size });
    },
    enabled: !!token && isMounted, // Only fetch if token exists and component is mounted
    staleTime: 30 * 1000, // 30 seconds
  });

  // Sync fetched data with WebSocket state
  useEffect(() => {
    if (queryData?.items) {
      setWsItems(queryData.items);
    }
  }, [queryData?.items, setWsItems]);

  // Use WebSocket items if available, otherwise use query data
  const data = useMemo(() => {
    if (wsItems.length > 0) {
      return wsItems;
    }
    return queryData?.items || [];
  }, [wsItems, queryData?.items]);

  // Update filters
  const setFilters = useCallback(
    (newFilters: Record<string, any>) => {
      setFiltersState((prev) => {
        const merged = { ...prev, ...newFilters };
        // Ensure page and page_size are always present
        if (merged.page === undefined) merged.page = prev.page || initialPage;
        if (merged.page_size === undefined)
          merged.page_size = prev.page_size || initialPageSize;
        return merged;
      });
    },
    [initialPage, initialPageSize]
  );

  // Update page
  const setPage = useCallback((newPage: number) => {
    setFiltersState((prev) => ({ ...prev, page: newPage }));
  }, []);

  // Update page size
  const setPageSize = useCallback((newPageSize: number) => {
    setFiltersState((prev) => ({ ...prev, page: 1, page_size: newPageSize }));
  }, []);

  // Manual refetch
  const manualRefetch = useCallback(async () => {
    await refetch();
  }, [refetch]);

  return {
    data,
    loading: !isMounted || isLoading || isPending, // Show loading until mounted to prevent hydration mismatch
    error: queryError ? (queryError instanceof Error ? queryError.message : 'Unknown error') : null,
    filters: (() => {
      // Return filters without page/page_size for DataTableFilters
      const { page: _, page_size: __, ...filterValues } = filters;
      return filterValues;
    })(),
    setFilters,
    pagination: {
      page,
      page_size,
      total: queryData?.total || 0,
    },
    setPage,
    setPageSize,
    refetch: manualRefetch,
  };
}
