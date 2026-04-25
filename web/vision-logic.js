/**
 * vision-logic.js
 * 
 * Objectives:
 * 1. Implement centroid (質心) calculation for edge detection/tracking.
 * 2. Implement dynamic quality switching strategy.
 */

class VisionSystem {
    constructor(esp32Url) {
        this.esp32Url = esp32Url;
        this.currentQuality = 80;
    }

    /**
     * Set JPEG Quality on the ESP32-CAM
     * @param {number} q - Quality value (10-63, lower is better quality in ESP32 context, 
     *                     but usually README refers to 0-100 scale. We'll map it.)
     */
    async setQuality(q) {
        console.log(`Setting quality to: ${q}`);
        try {
            await fetch(`${this.esp32Url}/quality?val=${q}`);
            this.currentQuality = q;
        } catch (e) {
            console.error("Failed to set quality", e);
        }
    }

    /**
     * Calculate centroid of a binary image or specific color mask
     * @param {ImageData} imageData 
     */
    calculateCentroid(imageData) {
        // TODO: Implement centroid calculation logic
        // x = sum(x_i) / N, y = sum(y_i) / N
        return { x: 0, y: 0 };
    }

    /**
     * Adaptive Strategy based on motion or state
     * @param {number} motorSpeed 
     */
    updateAdaptiveStrategy(motorSpeed) {
        // TODO: Implement "靜態細節優先，動態流暢優先"
        // if (motorSpeed === 0) this.setQuality(10); // High quality
        // else this.setQuality(30); // Lower quality for higher FPS
    }
}

const vision = new VisionSystem('http://192.168.x.x'); // Replace with actual ESP32 IP
