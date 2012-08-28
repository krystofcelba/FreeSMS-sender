import QtQuick 1.1 
import com.nokia.meego 1.0


PageStackWindow { 
	id : rootWindow
    initialPage: mainPage
    MainPage { 
        id: mainPage 
    }
	ToolBarLayout { 
        id: commonTools 
        visible: true 
        ToolIcon { 
            platformIconId: "toolbar-view-menu" 
            anchors.right: (parent === undefined) ? undefined : parent.right 
            onClicked: (myMenu.status == DialogStatus.Closed) ? myMenu.open() : myMenu.close() 
        } 
    }
    Menu { 
        id: myMenu 
        visualParent: pageStack 
        MenuLayout { 
            MenuItem { text: qsTr("Sample menu item") } 
            MenuItem { text: qsTr("Sample menu item1") } 
            MenuItem { text: qsTr("Sample menu item2") } 
        } 
    } 
	function showCaptcha() {
		captchaDialog.captchaContent = "image://captcha/" + Math.random().toString(); //Prevent image caching
		captchaDialog.captchaFieldText = ""
		captchaDialog.open();
	}

	Dialog {
		id: captchaDialog
		property alias captchaContent: captchaImage.source
		property alias captchaFieldText: captchaField.text
		//title:

		onAccepted: {
			helper.setCaptcha(captchaField.text)
		}
		onRejected: {
			helper.cancelSendingSMS()
		}

		content:Item {
			id: name
			height: captchaImage.height + 5 + captchaField.height
			width: parent.width
			Image {
				anchors {
					left: parent.left; right: parent.right
					margins: 5
				}
				id: captchaImage
			}
			TextField {
				id: captchaField
				placeholderText: qsTr("Type the text in the picture")
				anchors {
					top: captchaImage.bottom
					left: parent.left; right: parent.right
					margins: 5
				}
			}
		}
		
		buttons: ButtonRow {
			style: ButtonStyle { }
			anchors.horizontalCenter: parent.horizontalCenter
			Button {text: "OK"; onClicked: captchaDialog.accept()}
		}
	}
}
