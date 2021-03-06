import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.4

Window {
    id: window
    visible: true
    width: 1024
    height: 700
    title: qsTr("Hello World")
  
    Component.onCompleted: {
      main.onQtCompleted()
      window.title = 'qHalView ' + main.filename
    }

    Item {
        id: appContainer
        anchors.left: parent.left
        height: parent.height
        anchors.right: parent.right
        y: 0
        //anchors.top: parent.top
        //anchors.bottom: inputPanel.top
        
        
        ListView {
             id: lv
             anchors.fill: parent; 
             model: hal
             clip: true
             cacheBuffer:0
             delegate: Item {
                 height: 40; 
                 width: ListView.view.width
                 Rectangle{
                  id:bg
                  anchors.fill: parent
                  color: index % 2 == 1 ? '#111' : '#222' 
                 }
                 Rectangle{
                  id:lineNum
                  anchors.left: parent.left
                  width:50
                  height: parent.height - 1
                  color: 'lightgrey'
                  Text{
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 20
                    color: 'black'
                    text: model.i
                  }
                 }
                 Text {
                  id:tt
                  anchors.left: lineNum.right
                  text: model.line
                  font.pixelSize: 26
                  color: 'white'
                 }
                 Rectangle{
                  anchors.right: parent.right
                  anchors.rightMargin: 5
                  anchors.verticalCenter: parent.verticalCenter
                  width:120
                  height: parent.height - 2
                  color: value.text == 'False' ? 'red' : value.text == 'True' ? 'green' : value.text == '' ? bg.color :'grey'
                  Text{
                    id:value
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 25
                    color: 'black'
                   }
                 }
                 
                 Timer{
                   id: delegateTimer
                   interval: 300
                   repeat: true
                   running: true
                   onTriggered: {
                     value.text = main.refresh(model.line)
                   }
                 }
             }
         }

    } //item appContainer
} //window
