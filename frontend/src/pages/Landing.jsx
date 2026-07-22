import { Link } from 'react-router-dom'
import { Zap, Brain, BarChart3, ShoppingCart, ArrowRight, Activity } from 'lucide-react'

const FEATURES = [
  { icon: Brain,       title: 'AI-Powered Plans',    desc: 'Gemini generates personalised 7-day meal plans grounded in real nutritional data.'   },
  { icon: BarChart3,   title: 'Macro Tracking',       desc: 'Beautiful charts show your calorie, protein, carb, and fat breakdown at a glance.'    },
  { icon: Activity,    title: 'BMI & Health Metrics', desc: 'Scientific formulas — Mifflin-St Jeor BMR, TDEE, body fat estimate, ideal weight.'    },
  { icon: ShoppingCart,title: 'Grocery Lists',        desc: 'Auto-generated shopping lists from your meal plan so you never forget an ingredient.' },
]

const GOALS = ['Lose Fat', 'Build Muscle', 'Improve Health', 'Increase Endurance', 'Maintain Weight']

export default function Landing() {
  return (
    <div className="min-h-screen bg-surface overflow-x-hidden">
      {/* Navbar */}
      <nav className="fixed top-0 inset-x-0 z-50 border-b border-white/5 bg-surface/80 backdrop-blur-xl">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-brand-500 flex items-center justify-center shadow-glow-green">
              <Zap size={14} className="text-white" />
            </div>
            <span className="font-bold font-display text-white text-sm sm:text-base">AI Diet Planner</span>
          </div>
          <div className="flex items-center gap-2 sm:gap-3">
            <Link to="/login" className="btn-ghost text-xs sm:text-sm px-2.5 sm:px-4">Sign in</Link>
            <Link to="/register" className="btn-primary text-xs sm:text-sm px-3 sm:px-5">Get Started Free</Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-28 sm:pt-36 pb-16 sm:pb-20 px-4 sm:px-6 text-center relative overflow-hidden">
        {/* Glow orbs */}
        <div className="absolute top-20 left-1/4 w-72 sm:w-96 h-72 sm:h-96 bg-brand-600/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-40 right-1/4 w-64 sm:w-80 h-64 sm:h-80 bg-teal-600/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-brand-600/30 bg-brand-600/10 text-brand-400 text-xs font-medium mb-6 animate-in">
            <Zap size={11} />
            Powered by Google Gemini AI
          </div>

          <h1 className="text-3xl sm:text-5xl lg:text-7xl font-bold font-display text-white mb-6 leading-tight tracking-tight">
            Your Personal
            <span className="text-gradient block">AI Nutritionist</span>
          </h1>

          <p className="text-slate-400 text-sm sm:text-lg max-w-2xl mx-auto mb-8 sm:mb-10 leading-relaxed">
            Generate personalised 7-day meal plans in seconds. Backed by scientific formulas,
            a verified nutrition database, and your unique health profile.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-4 mb-10 w-full max-w-md mx-auto">
            <Link to="/register" className="btn-primary px-8 py-3 text-base gap-2 w-full sm:w-auto">
              Start for Free <ArrowRight size={18} />
            </Link>
            <Link to="/login" className="btn-secondary px-8 py-3 text-base w-full sm:w-auto">
              Sign In
            </Link>
          </div>

          {/* Goal pills */}
          <div className="flex flex-wrap justify-center gap-1.5 sm:gap-2">
            {GOALS.map((g) => (
              <span key={g} className="badge badge-green text-[11px] sm:text-xs">{g}</span>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 sm:py-20 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-10 sm:mb-14">
            <h2 className="text-2xl sm:text-3xl font-bold font-display text-white mb-3">
              Everything you need to reach your goals
            </h2>
            <p className="text-slate-400 text-xs sm:text-sm max-w-xl mx-auto">
              A full-stack diet planner built like a startup — not just a form that calls an API.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            {FEATURES.map(({ icon: Icon, title, desc }) => (
              <div key={title} className="card hover-lift group p-5">
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
      <section className="py-16 sm:py-20 px-4 sm:px-6">
        <div className="max-w-2xl mx-auto text-center card p-8 sm:p-12">
          <h2 className="text-2xl sm:text-3xl font-bold font-display text-white mb-4">Ready to transform your health?</h2>
          <p className="text-slate-400 text-xs sm:text-sm mb-6">Create your free account today and generate your first AI meal plan.</p>
          <Link to="/register" className="btn-primary px-8 py-3 text-base inline-flex">
            Get Started Now <ArrowRight size={18} />
          </Link>
        </div>
      </section>
    </div>
  )
}
