from sqlalchemy import Column, Integer, String, DateTime, Float
from external.aws_rds.db import Base 

class StakingDataHistory(Base):
    __tablename__ = "staking_data_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    network_address = Column(String, nullable=True)
    network_name = Column(String, nullable=True)
    network_category = Column(String, nullable=True)
    node_operator_address = Column(String, nullable=True)
    node_operator_name = Column(String, nullable=True)
    collateral_asset_address = Column(String, nullable=True)
    collateral_asset_symbol = Column(String, nullable=True)
    collateral_asset_price = Column(Float, nullable=True)
    amount_staked = Column(Float, nullable=True)
    amount_staked_usd = Column(Float, nullable=True)
    timestamp = Column(DateTime, nullable=True)

class StakingDataCurrent(Base):
    __tablename__ = "staking_data_current"

    id = Column(Integer, primary_key=True, autoincrement=True)
    network_address = Column(String, nullable=True)
    network_name = Column(String, nullable=True)
    network_category = Column(String, nullable=True)
    node_operator_address = Column(String, nullable=True)
    node_operator_name = Column(String, nullable=True)
    collateral_asset_address = Column(String, nullable=True)
    collateral_asset_symbol = Column(String, nullable=True)
    collateral_asset_price = Column(Float, nullable=True)
    amount_staked = Column(Float, nullable=True)
    amount_staked_usd = Column(Float, nullable=True)
    timestamp = Column(DateTime, nullable=True)


    