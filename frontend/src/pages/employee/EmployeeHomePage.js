
import DecisionFrame from '../../components/DecisionFrame';
import InfoBox from '../../components/InfoBox';
import React, { memo } from 'react';

const infoBoxes = [
  {
    title: 'Welcome to the Employee Portal',
    text: 'Access your schedule, manage PTO and sick days, and view important updates here.'
  },
  {
    title: 'Need to Book a Shift?',
    text: 'Use the Book Shift page to sign up for available shifts. Check your schedule for details.'
  },
  {
    title: 'Reimbursement Claims',
    text: 'Submit and track your reimbursement claims in the Finance section.'
  },
  {
    title: 'Support',
    text: 'Contact HR or your department manager for assistance with any issues.'
  }
];

/**
 * EmployeeHomePage
 * ----------------
 * This is the landing page for employees. It displays a set of informational boxes
 * to guide users to key features and resources within the employee portal.
 *
 * - infoBoxes: Array of objects, each representing a message or feature highlight.
 * - InfoBoxList: Memoized subcomponent for rendering the info boxes efficiently.
 * - DecisionFrame: Used for any future mutations (modals for actions).
 *
 * This page is read-only by default. Any future mutation must use DecisionFrame modal.
 */
/**
 * InfoBoxList
 * -----------
 * Memoized subcomponent to render a list of InfoBox components.
 * Props:
 *   - boxes: Array of info box objects with title and text.
 */
const InfoBoxList = memo(({ boxes }) => (
  <>
    {boxes.map((box, i) => (
      <InfoBox key={i} title={box.title} text={box.text} />
    ))}
  </>
));

/**
 * EmployeeHomePage Component
 * -------------------------
 * Renders the employee portal home with informational boxes.
 * All mutations must use the DecisionFrame modal for consistency and safety.
 */
const EmployeeHomePage = () => (
  <div>
    <h2>Employee Home</h2>
    <InfoBoxList boxes={infoBoxes} />
    {/* To mutate home page data, use DecisionFrame modal for all mutations. */}
  </div>
);

export default EmployeeHomePage;
