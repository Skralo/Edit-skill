import { Config } from '@remotion/cli/config';
import { existsSync } from 'node:fs';

Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(95);
// Claude Code cloud containers ship Chromium here; elsewhere Remotion downloads its own.
const CLOUD_CHROME = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
if (existsSync(CLOUD_CHROME)) Config.setBrowserExecutable(CLOUD_CHROME);
// The chrome sparkle is real WebGL (Three.js): headless Chromium needs ANGLE for it.
Config.setChromiumOpenGlRenderer('angle');
Config.setDelayRenderTimeoutInMilliseconds(120000);
Config.setConcurrency(4);
Config.setOverwriteOutput(true);
