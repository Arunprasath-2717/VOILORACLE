import { useState, useEffect, useCallback, useRef } from 'react';
import * as api from '../services/api';

/**
 * Generic hook for fetching data with loading/error states and auto-refresh.
 */
export function useApiData(fetchFn, deps = [], refreshInterval = 0) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const mountedRef = useRef(true);

  const fetchData = useCallback(async () => {
    try {
      const result = await fetchFn();
      if (mountedRef.current) {
        setData(result);
        setError(null);
        setLoading(false);
      }
    } catch (err) {
      if (mountedRef.current) {
        setError(err.message);
        setLoading(false);
      }
    }
  }, [fetchFn]);

  useEffect(() => {
    mountedRef.current = true;
    setLoading(true);
    fetchData();

    let interval;
    if (refreshInterval > 0) {
      interval = setInterval(fetchData, refreshInterval);
    }

    return () => {
      mountedRef.current = false;
      if (interval) clearInterval(interval);
    };
  }, [...deps, refreshInterval]);

  return { data, loading, error, refetch: fetchData };
}

/* ── Specific Data Hooks ──────────────────────────────── */

export function useMetrics(refreshMs = 15000) {
  return useApiData(() => api.getMetrics(), [], refreshMs);
}

export function useEvents(limit = 25, refreshMs = 10000) {
  return useApiData(() => api.getEvents(limit), [limit], refreshMs);
}

export function useArticles(limit = 100, refreshMs = 15000) {
  return useApiData(() => api.getArticles(limit), [limit], refreshMs);
}

export function useImpacts(refreshMs = 30000) {
  return useApiData(() => api.getImpacts(), [], refreshMs);
}

export function useStatus(refreshMs = 10000) {
  return useApiData(() => api.getStatus(), [], refreshMs);
}

export function useAISummary(refreshMs = 30000) {
  return useApiData(() => api.getAISummary(), [], refreshMs);
}

export function useEntities(refreshMs = 60000) {
  return useApiData(() => api.getEntities(), [], refreshMs);
}

export function useTrends(refreshMs = 30000) {
  return useApiData(() => api.getTrends(), [], refreshMs);
}

export function useAnomalies(refreshMs = 30000) {
  return useApiData(() => api.getAnomalies(), [], refreshMs);
}

export function useSectorDistribution(refreshMs = 30000) {
  return useApiData(() => api.getSectorDistribution(), [], refreshMs);
}

export function useIntelligence(limit = 25, refreshMs = 15000) {
  return useApiData(() => api.getIntelligence(limit), [limit], refreshMs);
}

export function usePipelineRuns(limit = 5, refreshMs = 15000) {
  return useApiData(() => api.getPipelineRuns(limit), [limit], refreshMs);
}

export function useGeoNews(query = null, refreshMs = 30000) {
  return useApiData(() => api.getGeoNews(query), [query], refreshMs);
}

export function useAlerts(hours = 6, refreshMs = 60000) {
  return useApiData(() => api.getAlerts(hours), [hours], refreshMs);
}

/* ── WebSocket Hook ───────────────────────────────────── */

export function useLiveUpdates() {
  const [liveData, setLiveData] = useState(null);
  const [connected, setConnected] = useState(true);

  useEffect(() => {
    let mounted = true;
    let failCount = 0;

    const fetchStatus = async () => {
      try {
        const res = await api.getMetrics();
        if (mounted) {
          setLiveData({ article_count: res.article_count });
          failCount = 0;
          if (!connected) setConnected(true);
        }
      } catch (e) {
        if (mounted) {
          failCount++;
          if (failCount >= 2) setConnected(false);
        }
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 8000);

    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, [connected]);

  return { liveData, connected };
}
