/**
 * InfoBox Component
 *
 * Displays a styled information box with a title and text.
 *
 * Props:
 *   - title: The title of the info box
 *   - text: The main text/content of the info box
 */
import React from 'react';
import './InfoBox.css';

/**
 * Main info box component.
 */
const InfoBox = ({ title, text }) => (
  <div className="info-box">
    <div className="info-box-title">{title}</div>
    <div className="info-box-text">{text}</div>
  </div>
);

export default InfoBox;
