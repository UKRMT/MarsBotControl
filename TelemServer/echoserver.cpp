/****************************************************************************
**
** Copyright (C) 2016 Kurt Pattyn <pattyn.kurt@gmail.com>.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the QtWebSockets module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/
#include "echoserver.h"
#include "QtWebSockets/qwebsocketserver.h"
#include "QtWebSockets/qwebsocket.h"
#include <QtCore/QDebug>

QT_USE_NAMESPACE

//! [constructor]
EchoServer::EchoServer(quint16 port, bool debug, QObject *parent) :
    QObject(parent),
    m_pWebSocketServer(new QWebSocketServer(QStringLiteral("Echo Server"),
                                            QWebSocketServer::NonSecureMode, this)),
    m_debug(debug)
{
    if (m_pWebSocketServer->listen(QHostAddress::Any, port)) {
        if (m_debug)
            qDebug() << "Echoserver listening on port" << port;
        connect(m_pWebSocketServer, &QWebSocketServer::newConnection,
                this, &EchoServer::onNewConnection);
        connect(m_pWebSocketServer, &QWebSocketServer::closed, this, &EchoServer::closed);
    }

    telemTimer = new QTimer(this);
    connect(telemTimer, SIGNAL(timeout()), this, SLOT(sendTelem()));

    // intitialize motor values to keep track of websocket commands
    motorVals[0] = 0;
    motorVals[1] = 0;
    motorVals[2] = 0;
    motorVals[3] = 0;

    // make a serial control object
    // SET THE SERIAL PORT SETTINGS
    serialPort.setPortName("/dev/ttyS0");
    serialPort.setBaudRate(QSerialPort::Baud115200);
    serialPort.setDataBits(QSerialPort::Data8);
    serialPort.setStopBits(QSerialPort::OneStop);
    serialPort.setParity(QSerialPort::NoParity);
    serialPort.setFlowControl(QSerialPort::NoFlowControl);

    // CONNECT THE SERIAL PORT TO THE READY READ SLOT
    connect(&serialPort, SIGNAL(readyRead()), this, SLOT(onReadyReadSerial()));

    if (!serialPort.open(QIODevice::ReadWrite)) {
        qDebug() << "cannot open serial port";
    } else {
        qDebug() << "opened serial port";
    }

}
//! [constructor]

EchoServer::~EchoServer()
{
    m_pWebSocketServer->close();
    qDeleteAll(m_clients.begin(), m_clients.end());
}

void EchoServer::onReadyReadSerial()
{
    // READ THE CURRENTLY AVAILABLE BYTES FROM THE PORT
    QByteArray byteArray = serialPort.readAll();

    if (byteArray.isEmpty() == false) {
        // SEND THE BYTES TO THE TCP CLIENT
        qDebug() << byteArray;
    } else {
        qDebug() << "INFO:: read no bytes from serial!";
    }

}

//! [onNewConnection]
void EchoServer::onNewConnection()
{
    QWebSocket *pSocket = m_pWebSocketServer->nextPendingConnection();

    connect(pSocket, &QWebSocket::textMessageReceived, this, &EchoServer::processTextMessage);
    connect(pSocket, &QWebSocket::binaryMessageReceived, this, &EchoServer::processBinaryMessage);
    connect(pSocket, &QWebSocket::disconnected, this, &EchoServer::socketDisconnected);

    m_clients << pSocket;
}
//! [onNewConnection]

//! [processTextMessage]
void EchoServer::processTextMessage(QString message)
{
  // parse the subscribe message  
  // pase message as json

  static QString prop;

  qDebug() << "got " << message;
  
  if (message.startsWith("subscribe")) {
      prop = message.split(' ').last();

      qDebug() << "socket wants info on " << prop;

      m_props << prop;

      if (!telemTimer->isActive() ){
	qDebug() << "starting timer";
	telemTimer->start(1000);
      }

  } else if (message.startsWith("unsubscribe")) {
    prop = message.split(' ').last();

    qDebug() << "unsubscribing from " << prop;
    
    if (m_props.indexOf(prop) != -1) {
      m_props.erase(m_props.begin()+m_props.indexOf(prop));
    }
    
    if (telemTimer->isActive() && m_props.isEmpty()) {
      qDebug() << "Stopping timer";
      telemTimer->stop();
    }
  } else if( message.startsWith("publish")) {
    prop = message.split(' ').last();
    qDebug() << "got publish from motors, i should handle this better";

  } else if(message.startsWith("M")) {
    
    qDebug() << "got command for motor " << message;

    for(int mc=0;mc<4;mc++){
      int temp =  message.mid(mc*4+2,3).toInt();
      int dir = message.mid(mc*4+1,1).toInt();

      if( dir==2 ){
	motorVals[mc] = 0;
      } else if(temp>0) {
	temp *= (dir==0) ? 1 : -1;	
	motorVals[mc]=temp;
      }
    }

    QString newString = "M";
    for( int mc=0; mc<4;mc++ ){
      newString.append(motorVals[mc]<=0 ? "1" : "0");
      newString.append(QString::number((motorVals[mc]<0)?motorVals[mc]*-1:motorVals[mc]).rightJustified(3,'0'));
    }
    newString.append('\n');
    
    QByteArray arr;
    arr.append(newString);
    serialPort.write(arr);

     qDebug() << "sent" << arr;
    
  } else {
    qDebug() << "not recognized";
  }
}
//! [processTextMessage]

void EchoServer::sendTelem()
{
  static int val = 77;
  QString fmt = "yyyy-MM-dd hh:mm:ss";
  QString now = QDateTime::currentDateTime().toString(fmt);

  for (int i=0; i<m_props.size(); i++){
    val = val + ((qrand() % 10)-5);
    val = val > 120 ? 120 : val < 50 ? 50 : val;
    QString prop = m_props[i];
    QJsonObject ob{{"timestamp",now},{"value",val},{"id",QString(prop)}};
    QJsonDocument doc(ob);
    QString resp(doc.toJson(QJsonDocument::Compact));

    qDebug() << "sending " << resp;
    
    QWebSocket *pClient = qobject_cast<QWebSocket *>(m_clients[0]);
    pClient->sendTextMessage(resp);
  }

  
}
  

//! [processBinaryMessage]
void EchoServer::processBinaryMessage(QByteArray message)
{
    QWebSocket *pClient = qobject_cast<QWebSocket *>(sender());
    if (m_debug)
        qDebug() << "Binary Message received:" << message;
    if (pClient) {
        pClient->sendBinaryMessage(message);
    }
}
//! [processBinaryMessage]

//! [socketDisconnected]
void EchoServer::socketDisconnected()
{
    QWebSocket *pClient = qobject_cast<QWebSocket *>(sender());
    if (m_debug)
        qDebug() << "socketDisconnected:" << pClient;
    if (pClient) {
        m_clients.removeAll(pClient);
        pClient->deleteLater();
    }
}
//! [socketDisconnected]
