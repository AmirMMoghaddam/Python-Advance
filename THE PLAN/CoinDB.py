import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="p@sswordis1379",
        database="trade"
    )

def create_tables():
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Create BASIC table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS basecoins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        coin_name VARCHAR(255) NOT NULL,
        coin_sym VARCHAR(50) NOT NULL,
        coin_address VARCHAR(255) UNIQUE,
        blockchain VARCHAR(100),
        volume INT,
        market_cap INT,
        added_date DATE NOT NULL 
    )
    """)
    conn.commit()
    # Create COIN INFORMATION table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coin_information (
        chainId VARCHAR(255),
        dexId VARCHAR(255),
        url TEXT,
        pairAddress VARCHAR(255) UNIQUE,
        labels VARCHAR(255),
        baseToken_address VARCHAR(255),
        baseToken_name VARCHAR(255),
        baseToken_symbol VARCHAR(255),
        quoteToken_address VARCHAR(255),
        quoteToken_name VARCHAR(255),
        quoteToken_symbol VARCHAR(255),
        priceNative FLOAT,
        priceUsd FLOAT,
        txns_m5 TEXT,
        txns_h1 TEXT,
        txns_h6 TEXT,
        txns_h24 TEXT,
        volume_m5 INT,
        volume_h1 INT,
        volume_h6 INT,
        volume_h24 INT,
        priceChange_m5 FLOAT,
        priceChange_h1 FLOAT,
        priceChange_h6 FLOAT,
        priceChange_h24 FLOAT,
        liquidity_usd FLOAT,
        liquidity_base FLOAT,
        liquidity_quote FLOAT,
        fdv FLOAT,
        pairCreatedAt DATETIME
    )
    """)
    conn.commit()
    conn.close()

def add_to_base(coin_name, coin_sym, coin_address, blockchain, volume, market_cap, added_date):
    create_tables()
    conn = connect_to_db()
    cursor = conn.cursor()
    #print(volume)
    if volume == "--":
        volume = 0
    
    # Use INSERT ... ON DUPLICATE KEY UPDATE to insert or update the record
    cursor.execute("""
    INSERT INTO basecoins (coin_name, coin_sym, coin_address, blockchain, volume, market_cap, added_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        volume = VALUES(volume),
        market_cap = VALUES(market_cap)
    """, (coin_name, coin_sym, coin_address, blockchain, volume, market_cap, added_date))
    
    conn.commit()
    conn.close()

def get_all_basecoins():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)  # Enable dictionary cursor
    cursor.execute("SELECT * FROM basecoins")
    rows = cursor.fetchall()
    conn.close()
    return rows
def add_coin_info_to_db(coin_info):
    create_tables()
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Check if the pairAddress already exists
    cursor.execute("SELECT * FROM coin_information WHERE pairAddress = %s", (coin_info.pairAddress,))
    result = cursor.fetchone()
    labels = ""
    if isinstance(coin_info.labels, list):
        for label in coin_info.labels:
           labels = labels +label + ","
    else:
        labels = "None"
    if result:
        # Update the existing record
        cursor.execute("""
        UPDATE coin_information
        SET chainId = %s, dexId = %s, url = %s, labels = %s, baseToken_address = %s, baseToken_name = %s, baseToken_symbol = %s,
            quoteToken_address = %s, quoteToken_name = %s, quoteToken_symbol = %s, priceNative = %s, priceUsd = %s, txns_m5 = %s,
            txns_h1 = %s, txns_h6 = %s, txns_h24 = %s, volume_m5 = %s, volume_h1 = %s, volume_h6 = %s, volume_h24 = %s,
            priceChange_m5 = %s, priceChange_h1 = %s, priceChange_h6 = %s, priceChange_h24 = %s, liquidity_usd = %s,
            liquidity_base = %s, liquidity_quote = %s, fdv = %s, pairCreatedAt = %s
        WHERE pairAddress = %s
        """, (
            coin_info.chainId, coin_info.dexId, coin_info.url, labels, coin_info.baseToken_address,
            coin_info.baseToken_name, coin_info.baseToken_symbol, coin_info.quoteToken_address, coin_info.quoteToken_name,
            coin_info.quoteToken_symbol, coin_info.priceNative, coin_info.priceUsd, str(coin_info.txns_m5), str(coin_info.txns_h1),
            str(coin_info.txns_h6), str(coin_info.txns_h24), coin_info.volume_m5, coin_info.volume_h1, coin_info.volume_h6,
            coin_info.volume_h24, coin_info.priceChange_m5, coin_info.priceChange_h1, coin_info.priceChange_h6, coin_info.priceChange_h24,
            coin_info.liquidity_usd, coin_info.liquidity_base, coin_info.liquidity_quote, coin_info.fdv,
            datetime.fromtimestamp((coin_info.pairCreatedAt)/1000).strftime('%Y-%m-%d'), coin_info.pairAddress
        ))
    else:
        # Insert a new record
        cursor.execute("""
        INSERT INTO coin_information (chainId, dexId, url, pairAddress, labels, baseToken_address, baseToken_name,
            baseToken_symbol, quoteToken_address, quoteToken_name, quoteToken_symbol, priceNative, priceUsd, txns_m5,
            txns_h1, txns_h6, txns_h24, volume_m5, volume_h1, volume_h6, volume_h24, priceChange_m5, priceChange_h1,
            priceChange_h6, priceChange_h24, liquidity_usd, liquidity_base, liquidity_quote, fdv, pairCreatedAt)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            coin_info.chainId, coin_info.dexId, coin_info.url, coin_info.pairAddress,labels, coin_info.baseToken_address,
            coin_info.baseToken_name, coin_info.baseToken_symbol, coin_info.quoteToken_address, coin_info.quoteToken_name,
            coin_info.quoteToken_symbol, coin_info.priceNative, coin_info.priceUsd, str(coin_info.txns_m5), str(coin_info.txns_h1),
            str(coin_info.txns_h6), str(coin_info.txns_h24), coin_info.volume_m5, coin_info.volume_h1, coin_info.volume_h6,
            coin_info.volume_h24, coin_info.priceChange_m5, coin_info.priceChange_h1, coin_info.priceChange_h6, coin_info.priceChange_h24,
            coin_info.liquidity_usd, coin_info.liquidity_base, coin_info.liquidity_quote, coin_info.fdv,
            datetime.fromtimestamp((coin_info.pairCreatedAt)/1000).strftime('%Y-%m-%d')
        ))
    
    conn.commit()
    conn.close()

def get_all_coin_information():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)  # Enable dictionary cursor
    cursor.execute("SELECT * FROM coin_information")
    rows = cursor.fetchall()
    conn.close()
    return rows

