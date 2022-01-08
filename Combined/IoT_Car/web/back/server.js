const express = require('express');

const app = express();

const PORT = 8081;

const db = require('./models');

const server = require('http').createServer(app);
const io = require('socket.io')(server,{
    pingTimeout: 1,
    pingInterval: 100,
});

io.on('connection' , async function(socket) {
    const temp = await db['sensing_1'].findAll({
        attributes: ['num2'],
        limit:1,
        order : [["time","DESC"]]
    });

    const humi = await db['sensing_1'].findAll({
        attributes: ['num3'],
        limit:1,
        order : [["time","DESC"]]
    });
    
    let tempmsg = temp.map(e => {
        a = e.dataValues.num2*100
        return a.toFixed(1)
    })
    let humiMsg = humi.map(e => {
        a = e.dataValues.num3*100
        return a.toFixed(1)
    })

    if(tempmsg.length > 0){
        socket.emit('temp', tempmsg)
        socket.emit('humi', humiMsg)
    }
    
})


server.listen(PORT, () => console.log(`this server listening on ${PORT}`));