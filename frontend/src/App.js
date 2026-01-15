
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import EmployeeServicesLayout from './pages/employee/EmployeeServicesLayout';
import ProductCatalogPage from './pages/ProductCatalogPage';
import CategoryPage from './pages/CategoryPage';
import ProductDetailPage from './pages/ProductDetailPage';
import ProfilePage from './pages/ProfilePage';
import LoginPage from './pages/LoginPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import RegisterPage from './pages/RegisterPage';
import EmployeeHomePage from './pages/employee/EmployeeHomePage';
import FinancePage from './pages/employee/FinancePage';
import RequestsPage from './pages/employee/RequestsPage';
import PTOPage from './pages/employee/PTOPage';
import IncidentsPage from './pages/employee/IncidentsPage';
import EmployeeProfilePage from './pages/employee/EmployeeProfilePage';
import PersonalSchedulePage from './pages/employee/PersonalSchedulePage';
import BookShiftPage from './pages/employee/BookShiftPage';
import CreateReimbursementPage from './pages/employee/CreateReimbursementPage';
import ReimbursementListPage from './pages/employee/ReimbursementListPage';
import EmployeeReimbursementDetailPage from './pages/employee/ReimbursementDetailPage';
import PaymentSnapshotsPage from './pages/employee/PaymentSnapshotsPage';
import GetSchedulePage from './pages/employee/GetSchedulePage';
import SellerServicesLayout from './pages/seller/SellerServicesLayout';
import SellerHomePage from './pages/seller/SellerHomePage';
import SellerProductsPage from './pages/seller/SellerProductsPage';
import SellerOrdersPage from './pages/seller/SellerOrdersPage';
import SellerPayoutsPage from './pages/seller/SellerPayoutsPage';
import SellerReviewsPage from './pages/seller/SellerReviewsPage';
import SellerProfilePage from './pages/seller/SellerProfilePage';
import IssuesCatalogPage from './pages/finance/IssuesCatalogPage';
import IssueDetailPage from './pages/finance/IssueDetailPage';
import ReimbursementsCatalogPage from './pages/finance/ReimbursementsCatalogPage';
import FinanceReimbursementDetailPage from './pages/finance/ReimbursementDetailPage';


function HomePage() {
  return (
    <div>
      <a href="https://reactjs.org">learn react</a>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/catalog" element={<ProductCatalogPage />} />
          <Route path="/category/:id" element={<CategoryPage />} />
          <Route path="/product/:id" element={<ProductDetailPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          <Route path="/register" element={<RegisterPage />} />
          {/* Employee Services routes */}
          <Route path="/employee" element={<EmployeeServicesLayout />}>
            <Route index element={<EmployeeHomePage />} />
            <Route path="schedule" element={<GetSchedulePage />} />
            <Route path="finance" element={<FinancePage />} />
            <Route path="requests" element={<RequestsPage />} />
            <Route path="pto" element={<PTOPage />} />
            <Route path="incidents" element={<IncidentsPage />} />
            <Route path="profile" element={<EmployeeProfilePage />} />
            <Route path="personal-schedule" element={<PersonalSchedulePage />} />
            <Route path="book-shift" element={<BookShiftPage />} />
            <Route path="reimbursement/create" element={<CreateReimbursementPage />} />
            <Route path="reimbursements" element={<ReimbursementListPage />} />
            <Route path="reimbursement/:id" element={<EmployeeReimbursementDetailPage />} />
            <Route path="payment-snapshots" element={<PaymentSnapshotsPage />} />
          </Route>
          {/* Seller Portal: all /seller routes use SellerServicesLayout */}
          <Route path="/seller" element={<SellerServicesLayout />}>
            <Route index element={<SellerHomePage />} />
            <Route path="products" element={<SellerProductsPage />} />
            <Route path="orders" element={<SellerOrdersPage />} />
            <Route path="payouts" element={<SellerPayoutsPage />} />
            <Route path="reviews" element={<SellerReviewsPage />} />
            <Route path="profile" element={<SellerProfilePage />} />
          </Route>
          {/* Finance Department routes */}
          <Route path="/finance/issues" element={<IssuesCatalogPage />} />
          <Route path="/finance/issues/:id" element={<IssueDetailPage />} />
          <Route path="/finance/reimbursements" element={<ReimbursementsCatalogPage />} />
          <Route path="/finance/reimbursements/:id" element={<FinanceReimbursementDetailPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
