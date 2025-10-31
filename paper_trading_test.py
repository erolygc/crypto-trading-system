#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paper Trading Test - Gerçek zamanlı trading simulasyonu
Gate.io API ile gerçek veriler kullanarak paper trading testi
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from signal_generator import SignalGenerator
from technical_indicators import TechnicalIndicators
from position_sizing import PositionSizer

class PaperTrader:
    """Paper Trading sınıfı - Gerçek zamanlı simulasyon"""
    
    def __init__(self, initial_balance: float = 10000):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.positions = {}
        self.trades = []
        self.pnl_history = []
        self.signal_generator = SignalGenerator()
        self.position_sizer = PositionSizer()
        
    def start_simulation(self, data: Dict[str, pd.DataFrame], duration_days: int = 7):
        """Paper trading simulasyonu başlat"""
        print(f"🚀 Paper Trading Simülasyonu Başlatılıyor...")
        print(f"📊 Başlangıç Bakiyesi: ${self.initial_balance:,.2f}")
        print(f"📅 Süre: {duration_days} gün")
        
        # Multi-timeframe data analysis
        for i, (timestamp, row) in enumerate(data['1m'].iterrows()):
            if i % 60 == 0:  # Her saat
                self._analyze_and_trade(data)
                self._update_portfolio_value(data)
                
        return self._generate_performance_report()
        
    def _analyze_and_trade(self, data: Dict[str, pd.DataFrame]):
        """Analiz yap ve işlem kararı ver"""
        # Multi-timeframe signal generation
        signals = self.signal_generator.generate_consensus_signal(data)
        
        # Position sizing
        position_size = self.position_sizer.calculate_position_size(
            signal_strength=signals['confidence'],
            account_value=self.current_balance,
            risk_per_trade=0.02
        )
        
        # Execute trade based on signal
        if signals['signal'] == 'BUY' and position_size > 0:
            self._execute_buy_order('BTC/USDT', position_size)
        elif signals['signal'] == 'SELL':
            self._execute_sell_order('BTC/USDT')
            
    def _generate_performance_report(self) -> Dict:
        """Performans raporu oluştur"""
        total_return = (self.current_balance - self.initial_balance) / self.initial_balance * 100
        
        return {
            'initial_balance': self.initial_balance,
            'final_balance': self.current_balance,
            'total_return_pct': total_return,
            'total_trades': len(self.trades),
            'win_rate': self._calculate_win_rate(),
            'sharpe_ratio': self._calculate_sharpe_ratio(),
            'max_drawdown': self._calculate_max_drawdown()
        }
