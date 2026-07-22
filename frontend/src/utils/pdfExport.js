/**
 * PDF export utility using jsPDF.
 * Generates a clean text-based report of the meal plan.
 * Usage: exportPlanToPDF(plan)
 */
import jsPDF from 'jspdf'

export function exportPlanToPDF(plan) {
  const doc = new jsPDF({ unit: 'mm', format: 'a4' })
  const PW = 210
  const M  = 15  // margin

  const green  = [34, 197, 94]
  const white  = [255, 255, 255]
  const dark   = [15, 23, 42]
  const slate  = [100, 116, 139]

  let y = 0

  // ── Header ──────────────────────────────────────────────────────────────
  doc.setFillColor(...dark)
  doc.rect(0, 0, PW, 40, 'F')

  doc.setFillColor(...green)
  doc.roundedRect(M, 8, 10, 10, 2, 2, 'F')

  doc.setFontSize(16).setFont('helvetica', 'bold').setTextColor(...white)
  doc.text('AI Diet Planner', M + 14, 16)

  doc.setFontSize(9).setFont('helvetica', 'normal').setTextColor(...slate)
  doc.text('Personalised Nutrition Report', M + 14, 22)

  doc.setFontSize(20).setFont('helvetica', 'bold').setTextColor(...green)
  doc.text(plan.title || '7-Day Meal Plan', M, 34)
  y = 48

  // ── Targets ─────────────────────────────────────────────────────────────
  doc.setFillColor(30, 41, 59)
  doc.roundedRect(M, y, PW - M * 2, 18, 3, 3, 'F')

  doc.setFontSize(8).setFont('helvetica', 'normal').setTextColor(...slate)
  const targets = [
    `Calories: ${plan.target_calories} kcal`,
    `Protein: ${plan.target_protein_g}g`,
    `Carbs: ${plan.target_carbs_g}g`,
    `Fat: ${plan.target_fat_g}g`,
    `Water: ${Math.round((plan.target_water_ml || 2500) / 100) / 10}L`,
  ]
  targets.forEach((t, i) => {
    doc.text(t, M + 5 + i * 36, y + 11)
  })
  y += 26

  // ── Days ────────────────────────────────────────────────────────────────
  const days = [...new Set((plan.meals || []).map((m) => m.day_number))].sort()

  days.forEach((dayNum) => {
    const meals = (plan.meals || []).filter((m) => m.day_number === dayNum)

    // Day header
    if (y > 260) { doc.addPage(); y = M }

    doc.setFillColor(...green)
    doc.rect(M, y, 2, 7, 'F')
    doc.setFontSize(10).setFont('helvetica', 'bold').setTextColor(...white)
    doc.text(`Day ${dayNum}`, M + 5, y + 5)
    y += 11

    meals.forEach((meal) => {
      if (y > 270) { doc.addPage(); y = M }

      // Meal type chip
      doc.setFontSize(7).setFont('helvetica', 'bold').setTextColor(...green)
      doc.text(meal.meal_type.toUpperCase().replace('_', '-'), M + 3, y + 4)

      // Meal name
      doc.setFontSize(9).setFont('helvetica', 'bold').setTextColor(...white)
      doc.text(meal.name, M + 28, y + 4)

      // Macros
      doc.setFontSize(7.5).setFont('helvetica', 'normal').setTextColor(...slate)
      doc.text(
        `${meal.calories} kcal · P ${meal.protein_g}g · C ${meal.carbs_g}g · F ${meal.fat_g}g`,
        M + 3,
        y + 9,
      )

      y += 14
    })

    y += 4
  })

  // ── Grocery list ────────────────────────────────────────────────────────
  const grocery = plan.grocery_items || []
  if (grocery.length > 0) {
    if (y > 240) { doc.addPage(); y = M }

    doc.setFontSize(10).setFont('helvetica', 'bold').setTextColor(...white)
    doc.text('Grocery List', M, y)
    y += 8

    grocery.forEach((item, i) => {
      if (y > 280) { doc.addPage(); y = M }
      doc.setFontSize(8).setFont('helvetica', 'normal').setTextColor(...slate)
      doc.text(`• ${item.name} — ${item.quantity} ${item.unit}`, M + 3, y)
      y += 5.5
    })
  }

  // ── Footer ───────────────────────────────────────────────────────────────
  const pageCount = doc.getNumberOfPages()
  for (let p = 1; p <= pageCount; p++) {
    doc.setPage(p)
    doc.setFontSize(7).setFont('helvetica', 'normal').setTextColor(...slate)
    doc.text(
      `AI Diet Planner · Generated ${new Date().toLocaleDateString()} · Page ${p} of ${pageCount}`,
      PW / 2,
      295,
      { align: 'center' },
    )
  }

  const filename = `diet-plan-${plan.start_date || 'export'}.pdf`
  doc.save(filename)
}
