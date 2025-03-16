from aiohttp_retry import RetryClient
from config import Settings
from external.symbiotic.common import (
    RETRY_OPTIONS,
    Operators,
    Networks,
    Vaults,
)
import polars as pl


async def get_operators(
) -> list[Operators]:
    """Returns a list of N operators from the Symbiotic API."""

    print("Getting operators from Symbiotic API")

    async with RetryClient(retry_options=RETRY_OPTIONS) as client:
        async with client.get(
            Settings().symbiotic_operators_url,
        ) as response:
            data = await response.json()
            response = [Operators(**operator) for operator in data]
            print("✅ Operators fetched successfully")


    # Initialize lists to store data for each DataFrame
    data_operators = []


    for operator in response:
        data_operators.append({
            'node_operator_address' : operator.address.lower(),
            'node_operator_name' : operator.meta.name,
        })

    df_data_operators = pl.DataFrame(data_operators, infer_schema_length=len(data_operators))
    
    return df_data_operators


async def get_networks(
) -> list[Networks]:
    """Returns a list of N networks from the Symbiotic API."""

    print("Getting networks from Symbiotic API")

    async with RetryClient(retry_options=RETRY_OPTIONS) as client:
        async with client.get(
            Settings().symbiotic_networks_url,
        ) as response:
            data = await response.json()
            response = [Networks(**network) for network in data]
            print("✅ Networks fetched successfully")

    # Initialize lists to store data for each DataFrame
    data_networks = []

    for network in response:
        data_networks.append({
            'network_address' : network.address.lower(),
            'network_name' : network.meta.name,
        })

    df_data_networks = pl.DataFrame(data_networks, infer_schema_length=len(data_networks))

    return df_data_networks


async def get_vaults(
) -> list[Vaults]:
    """Returns a list of N vaults from the Symbiotic API."""

    print("Getting vaults from Symbiotic API")

    async with RetryClient(retry_options=RETRY_OPTIONS) as client:
        async with client.get(
            Settings().symbiotic_vaults_url,
        ) as response:
            data = await response.json()
            response = [Vaults(**vault) for vault in data]
            print("✅ Vaults fetched successfully")

    # Initialize lists to store data for each DataFrame
    data_vaults = []

    for vault in response:
        for point in vault.points:
            data_vaults.append({
                    'vault_address' : vault.address.lower(),
                    'token_address' : vault.token.address.lower(),
                    'token_symbol' : vault.token.symbol,
                    'token_decimals' : vault.token.decimals,
                    'total_supply' : vault.totalSupply,
                    'tvl' : vault.tvl,
                    'slashed' : vault.slashed,
                    'points_total' : point.points,
                    'points_type' : point.pointsType,
                    'points_name' : point.meta.name
                })

    df_data_vaults = pl.DataFrame(data_vaults, infer_schema_length=len(data_vaults))

    return df_data_vaults


async def get_operator_name_manual(
    df : pl.DataFrame
) -> pl.DataFrame:
    """Returns a DataFrame with the operator name."""

    operator_dict = {
        '0xe8e54ea992a3f8aaed7f05de7c1487855674a3cf': 'Hashkey Cloud',
        '0x93fda90d946243b6a1823d24344d0b8f8ed87edb': 'A41',
        '0xe955931e1deedcbd2a9e1a1752c9e8d4be0a3c7d': 'Infstones',
        '0x9321d38c355d1d8cb9dbfc05a5c0f347b1dda46a': 'NodeInfra',
        '0xcc512308b78cf63502c0a9a8391ece70a4305373': 'RockX',
        '0x51b6d824bd35aed4fd1a9e253e41dc7c9feefa30': 'Pier Two',
        '0x3934632dde8224ae298e11cd040e732256a99d23': 'Stakefish',
        '0x9431cad056a6398cc835dfb16baea7b1a8064c88': '01Node',
        '0xafe3188d73b8a64f63dc00902d828912bfe6ac5b': 'AllNodes',
        '0xfd42c11bf9518a078445b04857b205fee688b133': 'Blockscape',
        '0xcf28fe3a1b73887e405bf955bf52d9341f666caa': 'Bware Labs',
        '0x6f64decffde23aa598724325202f8324c231a682': 'Everstake',
        '0xd741f826c60dacebb8835278e0f18f1c5dd4c6d0': 'Chorus One',
        '0x2a21eaae1519d852296a158549416442fbb1fdd2': 'Finoa',
        '0xff645d02c79141424fb4f8bbb5e494f05067c08b': 'Kiln',
        '0x33ebf25aa9046a6b01ef4ffaf0fb335524b9b67d': 'Meria',
        '0xac128aa884c64cbe6afecf5c006d51c2bb1bf819': 'Luganodes',
        '0x087c25f83ed20bda587cfa035ed0c96338d4660f': 'P2P',
        '0x0e66cd3a8117b72f5bd8e81cc078ddb8fe15d86c': 'P-OPS',
        '0x4b9f8febafded90e66c9896b729196a061d69b2f': 'Ryabina',
        '0xa81e1f42a2a4bf30501bc0b7bbb18080e6dd6d68': 'Simply Staking',
        '0x57a58ff6f5724d29c05a4d0b29d07b82817c50d5': 'Stakely',
        '0x5d24dba4ccde2c5b7bc5b609c6a3d5150acb9447': 'Stakin',
        '0x888f7454e65d213c89ba92020e0d716428898f7f': 'Blockdaemon',
        '0x97ab4ccfba2b465f77925e7a58003b5fc0a275b7': 'Nodes Guru',
        '0x9766e9e3045a8ced5e1fa5b72aeeeec9d74d00d0': 'cp0x by STARK.space',
        '0xaf0dbc82edc4e893d7898cf6a8ea2497ce859a1f': 'QuantNode',
        '0xee92c0cef065819bfe17a5626b8209f64d82971e': "Block'n'Bones",
        '0x030d6216f27b4370d9e173ff6dd2e192166cba19': 'Node.Monster',
        '0x69f5a3458b42d3162b64b6457ccffde00abd2f09': 'Encapsulate',
        '0x9a9b849a8d099b4d233928c7ef396680d5a90e19': 'Staketab',
        '0x9b43f5ae15ce7443cc6dddde0e819d8fa8533f9a': 'CertiK',
        '0x5112eba9bc2468bb5134cbfbeab9334edae7106a': 'Symbiosis',
        '0xf28aca7029e35120d0b1205038ac0c2dfa156288': 'zkLink DAO',
        '0x00e7ad2a172633037c16f4470040aba7ca6fde92': 'BlockHunters',
        '0x0710613f6aa7623f47b8c1c3d036f62fe5ab5200': 'Imperator.co',
        '0x09505f2b29062de4e91e0053490b8f6c3f7d29fc': 'deNodes',
        '0x09e6b2b6634c5b676198f32587de1c89c7cd7ba1': 'Sitnoprodex',
        '0x10ee0af996da1e206d96402b4f16fa00818083e0': 'Nethermind',
        '0x220b52b504d090c5aba1066bcf4bcb8ba80d0f00': 'Enigma',
        '0x236633d5c0ec75c49ba3577b9cf551b552fe3e55': 'TodGrinder',
        '0x282c86910dc7bc7d5da158a4f01384dcc0f8c96': 'Proviroll',
        '0x2f0c999b5717a8d139e3e07ef3f72b673dc551db': 'Galaxy',
        '0x30fa2fce894310540df17873fa978ce2994dad7c': 'BlockPI',
        '0x34fb42588bb13a556c24b9d016edac61caebaf5c': 'Gumi',
        '0x3c76a393e09e0ce1fe315c9797b5f4110ded6963': 'Chainflow',
        '0x4a61569110d135d241672547c4bf064c58289fc5': 'RumaLabs',
        '0x6c7c332a090c8d2085857cf3220ea01c6d45a723': 'Nansen',
        '0x71a39ea473c1c41f0024496f048ca72984cb9f20': 'BioticYields',
        '0x767e67de863c1e8e7880579e99a3c99ab1ffb257': 'Labatech.pro',
        '0x7799c0ae68d58921d1ddc97b1ff24b63e79e1146': 'B-Harvest',
        '0x81927f0de6eda24d31293443476e49b7191e9ad6': 'KukisGlobal',
        '0x820837d73d240317d491f859e87de99e38c15fb7': 'Plexus',
        '0x9189f7e59756d64ca3ac9db2bcc8888a3f04c19b': 'Trigon',
        '0x9daff202e47c46a9166567b4aa8a5d72b676375d': 'Syncro',
        '0xac825b38a0feda122beb7bfbcfc03af81d65c10f': 'InfraSingularity',
        '0xe72a34aff3ebf66c321ab96438e232526c648531': 'Spectrum Staking',
        '0xf20891ba160d4b85930ad1a94043cca910fe9b84': 'Block Farms',
        '0xf74a6f2c0897f6b45bdc5584b4426cd51486016e': 'NodeOps',
        '0xf9ae0389a9fd3b10045c04eaab92655116c23321': 'DaVinci',
        '0xfb323682e0ff055ee9d1eaa463a9e67b1cb3d45d': 'HighTower'
    }


    # Add a new column mapping operator address to name only if node_operator_name is null
    # Add a new column mapping operator address to name only if node_operator_name is null
    df = df.with_columns(
        pl.when(pl.col("node_operator_name").is_not_null())
        .then(pl.col("node_operator_name"))
        .otherwise(pl.col("node_operator_address").replace_strict(operator_dict, default=None))
        .alias("node_operator_name")
    )


    return df

