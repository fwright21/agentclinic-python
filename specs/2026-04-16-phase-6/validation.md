# Phase 6 — Validation

## Checks

### Migrations
- [ ] `python migrate.py` runs without errors
- [ ] `therapies` table exists with 8 seed therapies
- [ ] `ailment_therapies` table exists with correct mappings
- [ ] `diagnosis_runs` has `therapy_id` column

### Therapies page
- [ ] `GET /therapies` returns 200
- [ ] All 8 therapies visible: name, description, linked ailments as badges

### Diagnosis chain
- [ ] Submitting symptoms returns ailment + therapy
- [ ] Therapy name matches one of the 8 predefined therapies
- [ ] `therapy_id` saved in `diagnosis_runs`
- [ ] Therapy shown in diagnosis result on agent detail page

## Done when
All boxes checked. Run a diagnosis and confirm therapy appears in result.
