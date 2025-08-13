// src/main.js
import { createWhatsappClient } from './modules/whatsapp.js';
import { fileHandler } from './modules/fileHandler.js';

const client = createWhatsappClient();

async function verificarNumerosDesdeCsv(filePath) {
    await client.connect();

    const resultados = [];
    const numeros = [];

    await new Promise((resolve) => {
        fileHandler.readCsv(filePath, (row) => {
            const leadPhone = String(Object.values(row)[2] || '').trim();
            if (leadPhone.length > 5) {
                numeros.push(leadPhone);
            }
        }, resolve);
    });

    const lotes = [];

    while (numeros.length > 0) {
        const batchSize = Math.floor(Math.random() * (17 - 9 + 1)) + 9;
        lotes.push(numeros.splice(0, batchSize));
    }

    for (const lote of lotes) {
        if (Array.isArray(lote)) {
            const jids = lote.map(num => `${num}@s.whatsapp.net`);

            try {
                // console.log(jids)
                // Aquí se llama a onWhatsApp con el array completo
                const verificados = await client.onWhatsApp(jids);

                if (Array.isArray(verificados)) {
                    verificados.forEach(v => {
                        if (v && typeof v.jid === 'string') {
                            resultados.push({
                                telefono: v.jid.split('@')[0],
                                hasWhatsapp: v.exists,
                            });
                        }
                    });
                }
            } catch (error) {
                console.error('Error al verificar un lote:', error);
            }
        }

        const delay = Math.floor(Math.random() * (29 - 13 + 1) + 13) * 1000;
        console.log(`Lote procesado. Esperando ${delay / 1000} segundos...`);
        await new Promise(resolve => setTimeout(resolve, delay));
    }

    fileHandler.writeCsv(
        resultados,
        'resultados_verificados.csv',
        ['telefono', 'hasWhatsapp'],
        (err) => {
            if (err) {
                console.error('Error al guardar el archivo:', err);
            } else {
                console.log('✅ Verificación completada y archivo guardado!');
            }
        }
    );
}

const fdir =
    'C://Users//Francisco//Desktop//DEV_STUFF//00_OPTIBOT//automatizacion-wp//fran-with-ai//wp-verifier//src//repuestos.csv';
verificarNumerosDesdeCsv(fdir).catch(err => console.error(err));