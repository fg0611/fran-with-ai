// src/modules/fileHandler.js
import fs from 'fs'
import csv from 'csv-parser';
import { stringify as csvStringify } from 'csv-stringify';

export const fileHandler = {
    readCsv: (filePath, onDataCallback, onEndCallback) => {
        fs.createReadStream(filePath)
            .pipe(csv())
            .on('data', onDataCallback)
            .on('end', onEndCallback);
    },

    writeCsv: (data, filePath, header, callback) => {
        csvStringify(data, { header }, (err, output) => {
            if (err) return callback(err);
            fs.writeFile(filePath, output, callback);
        });
    }
};