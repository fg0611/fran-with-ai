// src/modules/whatsapp.js
import { makeWASocket, useMultiFileAuthState, DisconnectReason } from '@whiskeysockets/baileys';
import qrcode from 'qrcode-terminal';

export const createWhatsappClient = () => {
    let sock;
    let retries = 0;

    // La función connect ahora devuelve una promesa que se resuelve cuando la conexión está abierta
    function connect() {
        return new Promise(async (resolve, reject) => {
            const { state, saveCreds } = await useMultiFileAuthState('./auth');

            sock = makeWASocket({
                auth: state,
            });

            sock.ev.on('creds.update', saveCreds);

            sock.ev.on('connection.update', (update) => {
                const { connection, lastDisconnect, qr } = update;

                if (qr) {
                    console.log('📲 Escaneá este QR para conectar tu WhatsApp:\n');
                    qrcode.generate(qr, { small: true });
                }

                if (connection === 'close') {
                    retries += 1;
                    const reason = (lastDisconnect?.error)?.output?.statusCode;
                    if (reason === DisconnectReason.loggedOut) {
                        console.log("Sesión cerrada. Escanea el QR de nuevo.");
                        process.exit(0);
                    } else if (retries < 3) {
                        console.log("Reintentando conexión nro " + retries);
                        connect().then(resolve).catch(reject); // Recursivo para reintentar
                    } else {
                        reject(new Error('Conexión fallida después de 3 intentos.'));
                    }
                }

                if (connection === 'open') {
                    console.log('✅ WhatsApp ON');
                    resolve(); // Resuelve la promesa cuando la conexión se abre
                }
            });
        });
    }

    async function onWhatsApp(jids) {
        if (!sock) {
            throw new Error('WhatsApp client is OFF.');
        }
        // console.log('📤 Enviando JIDs para verificación:', jids);

        try {
            const result = await sock.onWhatsApp(...jids);

            const procesados = [];

            for (const r of result) {
                if (!r) continue;

                const destino = r.lid ? `${r.lid}` : r.jid;

                procesados.push({
                    consultado: r.jid.split('@')[0],
                    destino,
                    hasWhatsapp: !!r.exists,
                    tieneLid: !!r.lid
                });

                // 🔹 Si tiene LID, probamos enviar un mensaje
                if (r.lid) {
                    try {
                        console.log(`📨 Enviando mensaje de prueba a ${destino} (LID)`);
                        await sock.sendMessage(destino, { text: "Hola, somos Precios de Prepagas." });
                    } catch (err) {
                        console.error(`❌ Error enviando mensaje a ${destino}:`, err);
                    }
                }
            }

            console.log('📥 Resultado procesado:', procesados);
            return procesados;
        } catch (error) {
            console.error('❌ Error en sock.onWhatsApp:', error);
            throw error;
        }
    }



    // async function onWhatsApp(jids) {
    //     if (!sock) {
    //         throw new Error('WhatsApp client is OFF.');
    //     }
    //     // Línea de depuración: Imprime lo que se va a enviar
    //     // console.log('📤 Enviando JIDs para verificación:', jids);

    //     try {
    //         const result = await sock.onWhatsApp(...jids);

    //         // Línea de depuración: Imprime lo que se recibe
    //         console.log('📥 Resultado de la verificación:', result);

    //         return result;
    //     } catch (error) {
    //         console.error('❌ Error en sock.onWhatsApp:', error);
    //         throw error; // Propaga el error para que el main.js pueda manejarlo
    //     }
    // }

    return {
        connect,
        onWhatsApp,
    };
};