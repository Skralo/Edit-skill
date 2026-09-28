import { Composition } from 'remotion';
import { Film } from './film/Film';
import { FPS, H, TOTAL, W } from './film/timeline';

export const RemotionRoot: React.FC = () => (
  // The film: footage in its own colour + the white HUD edit in bursts + chrome outro (src/film).
  <Composition id="Film" component={Film} durationInFrames={TOTAL} fps={FPS} width={W} height={H} />
);
