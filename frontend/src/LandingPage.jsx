import React, { Suspense } from 'react';
import Spline from '@splinetool/react-spline';
import { Link } from 'react-router-dom';
import { ChevronRight, Sparkles, Globe, Shield, Zap, TrendingUp, LayoutDashboard } from 'lucide-react';
import './LandingPage.css';

const LandingPage = () => {
    return (
        <div className="landing-container">
            {/* Header / Navbar */}
            <nav className="landing-nav animate-fadeInDown">
                <div className="nav-logo">
                    <span className="logo-icon">🔮</span>
                    <span className="logo-text">VOILORACLE</span>
                </div>
                <div className="nav-links">
                    <a href="#features">Systems</a>
                    <a href="#intel">Intelligence</a>
                    <a href="#security">Security</a>
                    <Link to="/dashboard" className="nav-btn-primary">
                        <LayoutDashboard size={18} />
                        Access Dashboard
                    </Link>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-content">
                    <div className="hero-badge animate-fadeIn">
                        <Sparkles size={14} className="badge-icon" />
                        <span>NEXT-GEN AI INTELLIGENCE</span>
                    </div>
                    <h1 className="hero-title animate-slideInLeft">
                        Build an <span className="text-gradient">AI-Driven Future</span><br />
                        for Global Intelligence
                    </h1>
                    <p className="hero-subtitle animate-fadeIn" style={{ animationDelay: '0.2s' }}>
                        The ultimate neural matrix for real-time global event tracking,
                        predictive sector analytics, and cross-domain intelligence processing.
                        Engineered for accuracy, reliability, and unparalleled speed.
                    </p>
                    <div className="hero-cta animate-fadeIn" style={{ animationDelay: '0.3s' }}>
                        <Link to="/dashboard" className="cta-btn-main">
                            Get started for your business
                            <ChevronRight size={20} />
                        </Link>
                        <button className="cta-btn-secondary">
                            Discover more
                        </button>
                    </div>

                    <div className="hero-stats animate-fadeIn" style={{ animationDelay: '0.4s' }}>
                        <div className="hero-stat-item">
                            <span className="stat-val">3K+</span>
                            <span className="stat-lbl">Sectors Analyzed</span>
                        </div>
                        <div className="hero-stat-item">
                            <span className="stat-val">100M+</span>
                            <span className="stat-lbl">Signals Ingested</span>
                        </div>
                        <div className="hero-stat-item">
                            <span className="stat-val">0.4s</span>
                            <span className="stat-lbl">Response Latency</span>
                        </div>
                    </div>
                </div>

                <div className="hero-visual animate-slideInRight">
                    <Suspense fallback={<div className="spline-loading">Initializing 10D Neural Matrix...</div>}>
                        <div className="spline-wrapper">
                            <Spline scene="https://prod.spline.design/6Wq1Q7Ybe9hZ6vYd/scene.splinecode" />
                        </div>
                    </Suspense>
                    <div className="visual-overlay"></div>
                </div>
            </section>

            {/* Floating Features */}
            <section id="features" className="features-grid animate-fadeIn" style={{ animationDelay: '0.5s' }}>
                <div className="feature-card glass-panel">
                    <div className="feature-icon-wrapper blue">
                        <Globe size={24} />
                    </div>
                    <h3>Global Tracking</h3>
                    <p>Real-time surveillance across 13 major global news aggregators and deep web streams.</p>
                </div>
                <div className="feature-card glass-panel">
                    <div className="feature-icon-wrapper cyan">
                        <Zap size={24} />
                    </div>
                    <h3>Neural Processing</h3>
                    <p>Advanced DBSCAN clustering and sentence embeddings for sub-second event detection.</p>
                </div>
                <div className="feature-card glass-panel">
                    <div className="feature-icon-wrapper purple">
                        <Shield size={24} />
                    </div>
                    <h3>Disinfo Detector</h3>
                    <p>Proprietary RoBERTa models flagging disinformation and propaganda with 98.4% accuracy.</p>
                </div>
                <div className="feature-card glass-panel">
                    <div className="feature-icon-wrapper green">
                        <TrendingUp size={24} />
                    </div>
                    <h3>Impact Prediction</h3>
                    <p>Predictive modeling mapping sentiment shifts to market trajectories across 3000 sectors.</p>
                </div>
            </section>

            <div className="scroll-indicator animate-bounce">
                <span>SCROLL TO EXPLORE</span>
                <div className="mouse">
                    <div className="wheel"></div>
                </div>
            </div>

            <footer className="landing-footer">
                <p>&copy; 2026 VOILORACLE — ALL SYSTEMS NOMINAL. ENTERPRISE GRADE INTELLIGENCE.</p>
            </footer>
        </div>
    );
};

export default LandingPage;
