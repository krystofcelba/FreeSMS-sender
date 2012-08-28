import QtQuick 1.1 
import com.nokia.meego 1.0


Page { 
    tools: commonTools
	property alias toText: toField.text
	property alias contText: contentField.text
    
    TitleHeader{
		id: header
		title: qsTr("Free SMS")
    }
    TextField {
        id: toField
		placeholderText: qsTr("Recipient number")
		text: debug ? "605961068" : "";
        anchors {
            top: header.bottom
            left: parent.left; right: sendB.left
            margins: 5
		}
    }
    Button{ 
        id: sendB 
		width: 120
        anchors {
            top: header.bottom
            right: parent.right
            margins: 5
        }
        text: qsTr("Send") 
        onClicked: {
			helper.sendSMS(contentField.text, toField.text)
		}
    } 
    TextArea {
        id: contentField
        height: 80
		placeholderText: "Text"
		text: debug ? Math.random().toString() + "Text" : "";
        anchors {
            top: toField.bottom;
            left: parent.left; right: parent.right
            bottom: parent.bottom
            margins: 5
        }
    }
}

