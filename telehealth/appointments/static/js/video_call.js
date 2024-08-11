const startButton = document.getElementById('start-call');
const videoContainer = document.getElementById('video-container');
let localStream = null;
let peerConnection = null;

const configuration = {
    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
};

startButton.addEventListener('click', startCall);

async function startCall() {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        videoContainer.innerHTML = '<video id="local-video" autoplay muted></video><video id="remote-video" autoplay></video>';
        
        const localVideo = document.getElementById('local-video');
        localVideo.srcObject = localStream;

        peerConnection = new RTCPeerConnection(configuration);
        localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));

        peerConnection.ontrack = event => {
            const remoteVideo = document.getElementById('remote-video');
            remoteVideo.srcObject = event.streams[0];
        };

        peerConnection.onicecandidate = event => {
            if (event.candidate) {
                console.log('New ICE candidate:', event.candidate);
            }
        };

        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(offer);
        console.log('Sending offer:', offer);

    } catch (error) {
        console.error('Error accessing media devices.', error);
    }
}
