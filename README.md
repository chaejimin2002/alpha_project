# Alpha Project - Alpaca 자동매매 봇

Alpaca API를 활용한 SMA(Simple Moving Average) 전략 기반 자동매매 봇입니다.

## 🏗️ 전체 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Feed     │───▶│   Strategy      │───▶│   Risk Mgmt     │
│   (Alpaca API)  │    │   (SMA Signals) │    │   (TP/SL/Guard) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Main Bot Loop                                │
│              (bot.py - 핵심 실행 엔진)                          │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│   Broker        │
│   (Order Exec)  │
└─────────────────┘
```

## 🔄 워크플로우

### 1. 초기화 단계
- 환경변수 로드 (`.env` 파일)
- Alpaca API 연결 설정
- 로깅 설정
- 시장 상태 확인

### 2. 메인 루프 (bot.py)
```python
while RUN:
    # 1. 시장 시간 체크
    # 2. 데이터 수집 (OHLCV)
    # 3. 신호 계산 (SMA 크로스오버)
    # 4. 리스크 관리 체크
    # 5. 포지션 관리
    # 6. 주문 실행
    # 7. 대기 (poll_sec)
```

### 3. 데이터 수집 (datafeed.py)
- Alpaca API에서 실시간 주가 데이터 수집
- OHLCV 데이터를 pandas DataFrame으로 변환
- 설정된 시간프레임에 따른 캔들 데이터

### 4. 전략 신호 생성 (strategy.py)
- **SMA 크로스오버 전략**:
  - Fast SMA > Slow SMA → 매수 신호 (+1)
  - Fast SMA < Slow SMA → 매도 신호 (-1)
- 골든 크로스/데드 크로스 패턴 감지

### 5. 리스크 관리 (risk.py)
- **포지션 제한**: 최대 포지션 수 제한
- **Take Profit/Stop Loss**: 설정된 수익률/손실률에서 자동 청산
- **일일 손실 가드**: 일일 최대 손실 한도 도달 시 모든 포지션 청산

### 6. 주문 실행 (broker.py)
- Alpaca Trading API를 통한 실제 주문
- 시장가 주문 (Market Order)
- 포지션 청산 기능
- 계좌 정보 조회

## 🚨 안전장치

1. **시장 시간 체크**: 장외 시간 거래 방지
2. **중복 매매 방지**: 같은 캔들 내 중복 신호 무시
3. **일일 손실 가드**: 일일 최대 손실 한도
4. **포지션 제한**: 동시 보유 포지션 수 제한
5. **TP/SL**: 자동 손익 실현

## 📊 백테스팅 (backtest.py)
- 과거 데이터로 전략 성능 검증
- 수수료를 고려한 PnL 계산
- 초기 자본 10,000달러 기준 수익률 계산

## 🔧 주요 설정 (config.py)
- **거래 심볼**: 기본 BTC/USDT
- **시간프레임**: 1분봉
- **주문 크기**: 50달러
- **최대 포지션**: 1개
- **수수료**: 10bps
- **슬리피지**: 5bps

## 🚀 실행 방법

### 로컬 테스트
```bash
# 1) 코드 받기
git clone <your repo> && cd alpaca-autotrader

# 2) 환경변수 설정
cp .env.example .env
# .env 에 Alpaca 키/시크릿 입력 (paper=true 권장)

# 3) 로컬 실행(테스트)
pip install -r requirements.txt
python bot.py
```

### Docker 상시 실행
```bash
# 4) Docker로 상시 실행
docker compose up -d
docker compose logs -f trader
```

## 📁 프로젝트 구조

```
app/
├── bot.py          # 메인 실행 엔진
├── broker.py       # Alpaca API 브로커 인터페이스
├── strategy.py     # SMA 전략 구현
├── datafeed.py     # 데이터 수집 및 변환
├── risk.py         # 리스크 관리 모듈
├── config.py       # 설정 관리
└── backtest.py     # 백테스팅 모듈
```

## ⚠️ 주의사항

- **Paper Trading 권장**: 실제 자금으로 거래하기 전에 Paper Trading으로 충분히 테스트하세요
- **API 키 보안**: `.env` 파일을 안전하게 관리하고 Git에 커밋하지 마세요
- **리스크 관리**: 자동매매는 손실 위험이 있으므로 적절한 리스크 관리가 필요합니다
- **시장 상황**: 급격한 시장 변동 시 봇의 동작을 모니터링하세요