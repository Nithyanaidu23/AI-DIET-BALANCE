import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts'

const COLORS = {
  protein: '#3b82f6',
  carbs:   '#f59e0b',
  fat:     '#a855f7',
}

const CustomTooltip = ({ active, payload }) => {
  if (active && payload?.length) {
    return (
      <div className="card py-2 px-3 text-xs">
        <p className="font-semibold" style={{ color: payload[0].payload.color }}>
          {payload[0].name}
        </p>
        <p className="text-slate-300">{payload[0].value}g</p>
        <p className="text-slate-500">{payload[0].payload.calories} kcal</p>
      </div>
    )
  }
  return null
}

export default function NutritionChart({ protein, carbs, fat, size = 180 }) {
  const data = [
    { name: 'Protein', value: Math.round(protein), calories: Math.round(protein * 4), color: COLORS.protein },
    { name: 'Carbs',   value: Math.round(carbs),   calories: Math.round(carbs * 4),   color: COLORS.carbs   },
    { name: 'Fat',     value: Math.round(fat),      calories: Math.round(fat * 9),     color: COLORS.fat     },
  ].filter((d) => d.value > 0)

  const totalCalories = data.reduce((sum, d) => sum + d.calories, 0)

  return (
    <div className="relative">
      <ResponsiveContainer width="100%" height={size}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={size * 0.28}
            outerRadius={size * 0.42}
            paddingAngle={3}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={index} fill={entry.color} stroke="transparent" />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend
            iconType="circle"
            iconSize={8}
            formatter={(val) => <span className="text-xs text-slate-300">{val}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
      {/* Centre label */}
      <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none" style={{ paddingBottom: 20 }}>
        <p className="text-xl font-bold text-white">{totalCalories}</p>
        <p className="text-xs text-slate-400">kcal</p>
      </div>
    </div>
  )
}
