import { Connection, PublicKey } from '@solana/web3.js';
import { PhantomWalletAdapter } from '@solana/wallet-adapter-phantom';

export class WalletManager {
  constructor() {
    this.connection = new Connection(process.env.RPC_URL);
    this.wallet = new PhantomWalletAdapter();
  }

  async connect() {
    try {
      await this.wallet.connect();
      const response = await fetch('/billing/connect', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          address: this.wallet.publicKey.toString()
        })
      });
      return await response.json();
    } catch (error) {
      console.error('Wallet connection error:', error);
      throw error;
    }
  }

  async createPayment(plan) {
    const response = await fetch('/billing/solana-pay/create', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        address: this.wallet.publicKey.toString(),
        plan: plan
      })
    });
    return await response.json();
  }
}