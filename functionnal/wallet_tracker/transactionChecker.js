const Web3 = require('web3');
const CreateCsvWriter = require('csv-writer').createObjectCsvWriter;

const csvWriter = CreateCsvWriter({
    path: 'sent.csv',
    header: [
        {id: 'value', title: 'Value'},
        {id: 'timestamp', title: 'Timestamp'}
    ]
});

const csvWriterRecieved = CreateCsvWriter({
    path: 'recieved.csv',
    header: [
        {id: 'value', title: 'Value'},
        {id: 'timestamp', title: 'Timestamp'}
    ]
});

class TransactionChecker {
    web3;
    web3ws;
    account;
    subscription;

    constructor(projectId, account) {
        this.web3ws = new Web3(new Web3.providers.WebsocketProvider('wss://rinkeby.infura.io/ws/v3/' + projectId));
        this.web3 = new Web3(new Web3.providers.HttpProvider('https://rinkeby.infura.io/v3/' + projectId));
        this.account = account.toLowerCase();
    }

    

    subscribe(topic) {
        this.subscription = this.web3ws.eth.subscribe(topic, (err, res) => {
            if (err) console.error(err);
        });
    }

    watchTransactions() {
        console.log('Watching all pending transactions...');
        this.subscription.on('data', (txHash) => {
            setTimeout(async () => {
                try {
                    let tx = await this.web3.eth.getTransaction(txHash);
                    if (tx != null) {
                        if (this.account == tx.from.toLowerCase()) {
                            console.log("sent transaction");
                            console.log({address: tx.from, value: this.web3.utils.fromWei(tx.value, 'ether'), timestamp: new Date()});
                            const records = [
                                {value: this.web3.utils.fromWei(tx.value, 'ether'), timestamp: new Date()}
                            ];
                            csvWriter.writeRecords(records)
                                .then(() => {
                                    console.log('Done');
                                })
                        }
                    }
                    if (tx != null && tx.to != null) {
                        if (this.account == tx.to.toLowerCase()) {
                            console.log("recieved transaction");
                            console.log({address: tx.from, value: this.web3.utils.fromWei(tx.value, 'ether'), timestamp: new Date()});
                            const records = [
                                {value: this.web3.utils.fromWei(tx.value, 'ether'), timestamp: new Date()}
                            ];
                            csvWriterRecieved.writeRecords(records)
                                .then(() => {
                                    console.log('Done');
                                })
                        }
                    }
                } catch (err) {
                    console.error(err);
                }
            }, 60000)
        });
    }
}

let txChecker = new TransactionChecker('395b95cd458c4164af14c5dbc4d4a0b8', '0x2a3EB93322873FbCC160F9d51f3CC4d8F0F539ED');
txChecker.subscribe('pendingTransactions');
txChecker.watchTransactions();