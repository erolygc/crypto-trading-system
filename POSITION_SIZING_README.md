# Risk Yönetimi Dokümantasyonu

## Position Sizing Algoritmaları

### 1. Kelly Criterion
```python
# Kelly Formula: f = (bp - q) / b
# f: Fraction of capital to risk
# b: Odds received (profit/loss ratio)
# p: Probability of winning
# q: Probability of losing (1-p)
```

### 2. Risk Parity
- Her pozisyonun portfolio riskine katkısı eşit
- Volatilite bazlı pozisyon boyutlandırma
- Diversification maximization

### 3. ATR-Based Sizing
- Average True Range'e göre stop-loss mesafesi
- Volatilite-adaptive position sizing
- Market conditions'a duyarlı

### 4. Fixed Fractional
- Sabit yüzde risk (örn. %2 per trade)
- Simple ve etkili yöntem
- Drawdown kontrolü

### 5. Volatility Targeting
- Target portfolio volatility'e göre sizing
- GARCH models kullanımı
- Dynamic risk adjustment

### 6. Optimal f (Optimal Fraction)
- Monte Carlo simulation
- Maximum growth rate optimization
- Re-optimization gerekli

## Portfolio Optimization

### Modern Portfolio Theory (MPT)
- Risk-return optimization
- Efficient frontier construction
- Correlation-based diversification

### Black-Litterman Model
- Bayesian approach to MPT
- Market equilibrium integration
- Subjective views incorporation

## Risk Metrics

### Value at Risk (VaR)
- Historical simulation
- Parametric (Gaussian) method
- Monte Carlo simulation

### Conditional VaR (CVaR)
- Expected shortfall
- Tail risk measurement
- Regulatory compliance

### Beta Calculation
- Market correlation
- Systematic risk measurement
- Portfolio beta tracking

### Correlation Analysis
- Rolling correlation windows
- Regime change detection
- Diversification monitoring

## Implementation Example

```python
from position_sizing import PositionSizer
from risk_management import RiskManager

# Position sizer başlat
ps = PositionSizer()
rm = RiskManager()

# Kelly criterion ile sizing
kelly_size = ps.kelly_criterion(
    win_rate=0.65,
    avg_win=100,
    avg_loss=50
)

# Risk parity sizing
rp_size = ps.risk_parity(
    portfolio_vol=0.15,
    asset_vol=0.25,
    correlation=0.3
)

# VaR calculation
var_95 = rm.calculate_var(
    returns=portfolio_returns,
    confidence_level=0.95,
    method='historical'
)

print(f"Kelly Position Size: {kelly_size:.3f}")
print(f"Risk Parity Size: {rp_size:.3f}")
print(f"VaR (95%): ${var_95:,.2f}")
```

## Risk Limits

### Position Limits
- Maximum single position: 10% of portfolio
- Maximum sector exposure: 30% of portfolio
- Maximum correlation: 0.8 between positions

### Drawdown Limits
- Daily drawdown limit: 5%
- Weekly drawdown limit: 10%
- Monthly drawdown limit: 20%

### Volatility Limits
- Portfolio volatility ceiling: 25%
- Individual asset volatility: 50%

## Monitoring & Alerts

### Real-time Monitoring
- Position size alerts
- Risk limit breaches
- Correlation spikes
- Volatility threshold exceedances

### Performance Attribution
- Risk factor decomposition
- Alpha/beta analysis
- Style drift detection

## Best Practices

1. **Diversification**: Never put all eggs in one basket
2. **Position Sizing**: Size positions according to risk
3. **Stop Losses**: Always use protective stops
4. **Regular Review**: Reassess risk parameters regularly
5. **Stress Testing**: Test portfolio under extreme scenarios

## Emergency Procedures

### Market Crisis Response
- Reduce position sizes
- Increase cash allocation
- Activate hedging strategies
- Review stop-loss levels

### System Failure Protocol
- Manual trading overrides
- Position liquidation procedures
- Risk limit enforcement
- Communication plan

## Regulatory Compliance

### Risk Reporting
- Daily risk reports
- Monthly VaR statements
- Quarterly stress tests
- Annual risk review

### Capital Requirements
- Regulatory capital ratios
- Liquidity coverage ratio
- Leverage ratio monitoring
