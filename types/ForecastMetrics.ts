/**
 * 🎯 Metric Groups:
 * - Forecasting: Spend predictions + trendline
 * - Anomalies: Dates with unexpected spikes or drops
 * - Recommendations: LLM-based savings suggestions
 * - KPIs: Tailored metrics per persona
 * - Budget Insights: Track forecast vs. budget compliance
 */
export interface ForecastMetrics {
  // 1. Forecasting
  projectedSpendUSD: number;         // Total predicted spend (e.g., 6464.28)
  forecastedTrend: {
    date: string;                   // e.g., "2024-12-25"
    predictedCost: number;         // Daily forecasted cost
  }[];

  // 2. Anomaly Detection
  anomalyCount: number;             // Total # of anomalies
  anomalies: {
    date: string;
    cost: number;
    isAnomaly: boolean;
    deltaPercent?: number;         // Optional: spike % from baseline
  }[];

  // 3. Optimization / LLM Recommendations
  recommendations: {
    text: string;
    estimatedSavingsUSD?: number;  // e.g., 1200.00 if detected
    persona: 'FinOps' | 'CloudOps' | 'CIO';
    actionable: boolean;
  }[];

  // 4. KPI Summary (Role-Specific)
  kpis: {
    name: string;                    // e.g., "Idle VM Ratio"
    value: string | number;         // e.g., "12%", "3 VMs", 14.3
    category: 'Efficiency' | 'Spend' | 'Anomalies';
    persona: 'FinOps' | 'CloudOps' | 'CIO';
  }[];

  // 5. Budget Insights (Optional)
  budgetDriftUSD?: number;          // e.g., -300.00 (under budget)
  budgetCompliancePercent?: number; // e.g., 94.6%
} 