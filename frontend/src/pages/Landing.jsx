import { Link } from 'react-router-dom'
import { Zap, Brain, BarChart3, ShoppingCart, CheckCircle2, ArrowRight, Activity } from 'lucide-react'

const FEATURES = [
  { icon: Brain,       title: 'AI-Powered Plans',    desc: 'Gemini generates personalised 7-day meal plans grounded in real nutritional data.'   },
  { icon: BarChart3,   title: 'Macro Tracking',       desc: 'Beautiful charts show your calorie, protein, carb, and fat breakdown at a glance.'    },
  { icon: Activity,    title: 'BMI & Health Metrics', desc: 'Scientific formulas — Mifflin-St Jeor BMR, TDEE, body fat estimate, ideal weight.'    },
  { icon: ShoppingCart,title: 'Grocery Lists',        desc: 'Auto-generated shopping lists from your meal plan so you never forget an ingredient.' },
]

const GOALS = ['Lose Fat', 'Build Muscle', 'Improve Health', 'Increase Endurance', 'Maintain Weight']

export default function Landing() {
  return (
    <div className="min-h-screen bg-surface">
      {/* Navbar */}
      <nav className="fixed top-0 inset-x-0 z-50 border-b border-white/5 bg-surface/80 backdrop-blur-xl">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-brand-500 flex items-center justify-center shadow-glow-green">
              <Zap size={14} className="text-white" />
            </div>
            <span className="font-bold font-display text-white">AI Diet Planner</span>
          </div>
          <div className="flex items-center gap-3">
            <Link to="/login"    className="btn-ghost text-sm">Sign in</Link>
            <Link to="/register" className="btn-primary text-sm">Get Started Free</Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-32 pb-20 px-6 text-center relative overflow-hidden">
        {/* Glow orbs */}
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-brand-600/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-40 right-1/4 w-80 h-80 bg-teal-600/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-brand-600/30 bg-brand-600/10 text-brand-400 text-xs font-medium mb-6 animate-in">
            <Zap size={11} />
            Powered by Google Gemini AI
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold font-display text-white mb-6 leading-tight">
            Your Personal
            <span className="text-gradient block">AI Nutritionist</span>
          </h1>

          <p className="text-slate-400 text-lg max-w-2xl mx-auto mb-10 leading-relaxed">
            Generate personalised 7-day meal plans in seconds. Backed by scientific formulas,
            a verified nutrition database, and your unique health profile.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 mb-10">
            <Link to="/register" className="btn-primary px-8 py-3 text-base gap-3">
              Start for Free <ArrowRight size={18} />
            </Link>
            <Link to="/login" className="btn-secondary px-8 py-3 text-base">
              Sign In
            </Link>
          </div>

          {/* Goal pills */}
          <div className="flex flex-wrap justify-center gap-2">
            {GOALS.map((g) => (
              <span key={g} className="badge badge-green text-xs">{g}</span>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-bold font-display text-white mb-3">
              Everything you need to reach your goals
            </h2>
            <p className="text-slate-400 max-w-xl mx-auto">
              A full-stack diet planner built like a startup — not just a form that calls an API.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {FEATURES.map(({ icon: Icon, title, desc }) => (
              <div key={title} className="card hover-lift group">
                <div className="w-10 h-10 rounded-xl bg-brand-600/20 flex items-center justify-center mb-4 group-hover:bg-brand-600/30 transition-colors">
                  <Icon size={20} className="text-brand-400" />
                </div>
                <h3 className="font-semibold text-white mb-2 text-sm">{title}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6">
        <div className="max-w-2xl mx-auto text-center">
          <div className="card border-brand-600/30 bg-gradient-to-br from-brand-900/40 to-surface-card">
            <h2 className="text-2xl font-bold font-display text-white mb-3">
              Ready to transform your diet?
            </h2>
            <p className="text-slate-400 text-sm mb-6">
              Join thousands of users who are hitting their nutrition goals with AI-powered meal plans.
            </p>
            <Link to="/register" className="btn-primary mx-auto px-8">
              Create Free Account
            </Link>

            <div className="mt-6 flex items-center justify-center gap-6 text-xs text-slate-500">
              {['No credit card required', 'Instant plan generation', 'Cancel anytime'].map((t) => (
                <div key={t} className="flex items-center gap-1">
                  <CheckCircle2 size={11} className="text-brand-500" />
                  {t}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-surface-border py-8 px-6 text-center text-xs text-slate-600">
        <p>© {new Date().getFullYear()} AI Diet Planner. Built with ❤️ for portfolio & production.</p>
      </footer>
    </div>
  )
}
