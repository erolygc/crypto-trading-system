#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Signal Generator - Multi-timeframe consensus sistemi
Pump coinleri tespit eden akıllı sinyal üretim sistemi
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from technical_indicators import TechnicalIndicators

class SignalGenerator:
    """Multi-timeframe consensus signal generator"""
    
    def __init__(self):
        self.ti = TechnicalIndicators()
        self.timeframes = ['1m', '5m', '15m', '1h']
        self.weights = {'1m': 0.1, '5m': 0.2, '15m': 0.3, '1h': 0.4}
        
    def generate_consensus_signal(self, data: Dict[str, pd.DataFrame]) -> Dict:
        """Multi-timeframe consensus signal üretimi"""
        signals = {}
        
        for tf in self.timeframes:
            if tf in data:
                signals[tf] = self._analyze_timeframe(data[tf])
                
        return self._calculate_weighted_consensus(signals)
        
    def _analyze_timeframe(self, df: pd.DataFrame) -> Dict:
        """Tek timeframe analizi"""
        # RSI hesaplama
        rsi = self.ti.rsi(df['close'])
        
        # MACD hesaplama  
        macd_data = self.ti.macd(df['close'])
        
        # Bollinger Bands
        bb = self.ti.bollinger_bands(df['close'])
        
        return {
            'rsi': rsi.iloc[-1],
            'macd_signal': macd_data['signal'].iloc[-1],
            'bb_position': self._bollinger_position(df['close'].iloc[-1], bb),
            'volume_spike': self._detect_volume_spike(df)
        }
        
    def _calculate_weighted_consensus(self, signals: Dict) -> Dict:
        """Ağırlıklı consensus hesaplaması"""
        total_score = 0
        weights_used = 0
        
        for tf, data in signals.items():
            weight = self.weights[tf]
            score = self._calculate_signal_score(data)
            total_score += score * weight
            weights_used += weight
            
        if weights_used > 0:
            final_score = total_score / weights_used
        else:
            final_score = 0
            
        return {
            'signal': self._score_to_signal(final_score),
            'confidence': abs(final_score),
            'timeframe_breakdown': signals
        }
