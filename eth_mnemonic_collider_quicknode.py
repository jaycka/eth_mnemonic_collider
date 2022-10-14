from mnemonic import Mnemonic
from bip32utils import BIP32Key
from bip32utils import BIP32_HARDEN
import secp256k1Crypto as secp256k1
from Crypto.Hash import keccak
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://purple-proportionate-butterfly.discover.quiknode.pro/39b355a9c4f83f22c28ec3aa15ade800a3588b12/"))

mnemo = Mnemonic('english')
i=0
while True:
    i+=1
    words = mnemo.generate(strength=128)
    seed = mnemo.to_seed(words, passphrase="")

    xprv = BIP32Key.fromEntropy(seed, testnet=True).ExtendedKey()
    rootkey = BIP32Key.fromExtendedKey(xprv)
    priv = rootkey.ChildKey(44+BIP32_HARDEN).ChildKey(60+BIP32_HARDEN).ChildKey(0+BIP32_HARDEN).ChildKey(0).ChildKey(0).PrivateKey().hex()

    private_key_bytes = bytes.fromhex(priv)
    private_key = secp256k1.PrivateKey(private_key_bytes)
    public_key_bytes = private_key.pubkey.serialize(compressed=False)
    public_key_str = public_key_bytes.hex()
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(public_key_bytes[1:])
    h = keccak_hash.hexdigest()
    address = '0x' + h[-40:]
    address = w3.toChecksumAddress(address)
    balance = w3.eth.get_balance(address,'latest')
    print(i,priv,address,balance)
    if balance != 0:
        break
    