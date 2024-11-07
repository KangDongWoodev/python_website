// chat.js

document.addEventListener('DOMContentLoaded', function() {
    const roomName = document.querySelector('#room-name').dataset.roomName; // roomName 변수 설정
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/messenger/' + roomName + '/'
    );

    const messageInput = document.querySelector('#chat-message-input');
    const messageSubmitButton = document.querySelector('#chat-message-submit');

    // 입력 필드에 포커스 설정
    messageInput.focus();

    // WebSocket 연결 열렸을 때
    chatSocket.onopen = function(e) {
        console.log('WebSocket is open now.');
    };

    // WebSocket 연결 오류 발생 시
    chatSocket.onerror = function(e) {
        console.error('WebSocket error:', e);
    };

    // 메시지 제출 버튼 클릭 이벤트
    messageSubmitButton.addEventListener('click', function() {
        const message = messageInput.value;
        if (message.trim()) { // 공백 메시지 전송 방지
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInput.value = '';  // 메시지 전송 후 입력 필드 초기화
        }
    });

    // WebSocket으로부터 메시지 수신 시
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const message = data['message'];
        const sender = data['sender'];

        document.querySelector('#chat-log').innerHTML += (`
            <div class="chat-message">
                <strong>${sender}:</strong> ${message}
            </div>
        `);
    };

    // WebSocket 연결 종료 시
    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    // openChat 함수 추가
    window.openChat = function(userId) {
        // 팝업 창을 열고 해당 사용자와의 채팅을 초기화하는 코드
        const chatWindow = window.open(`/messenger/room/${userId}/`, 'ChatWindow', 'width=400,height=600');
        chatWindow.focus();
    }
});
