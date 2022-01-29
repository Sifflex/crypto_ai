const csv_p = require('csv-parse/sync');
const fs = require('fs');
const { parse } = require('path');

//const aes = AesEncryption();

let header = ["Recruteur_id", "Filiales", "Site_id", "Montant", "Debut", "Fin", "Quantite", "TypeAbo", "Suppr"]


let csv_file = fs.readFileSync(__dirname + '/../python_ia/Binance_BTCUSDT_minute.csv');

const parser = csv_p.parse(csv_file, {
    delimiter: ','
});


console.log(parser[0]);

module.exports = {
    parser
}
