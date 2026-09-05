const VIDEO_SRC =
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260514_135830_bb6491d1-9b66-4aec-9722-13b4dfe3fb46.mp4';

export function BackgroundVideo() {
  return (
    <video
      className="bg-video"
      src={VIDEO_SRC}
      autoPlay
      muted
      loop
      playsInline
      aria-hidden="true"
    />
  );
}
