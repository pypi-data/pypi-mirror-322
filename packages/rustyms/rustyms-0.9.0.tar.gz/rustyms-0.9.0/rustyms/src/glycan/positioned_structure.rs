//! Handle positioned glycan structures
use std::hash::Hash;

use itertools::Itertools;
use serde::{Deserialize, Serialize};

use super::MonoSaccharide;
use crate::{
    formula::{Chemical, MolecularFormula},
    fragment::{Fragment, FragmentType, GlycanBreakPos, GlycanPosition},
    molecular_charge::CachedCharge,
    system::usize::Charge,
    AminoAcid, Model, Multi, SequencePosition,
};

use crate::uom::num_traits::Zero;

/// Rose tree representation of glycan structure
#[derive(Debug, Eq, PartialEq, Clone, Hash, Serialize, Deserialize)]
pub struct PositionedGlycanStructure {
    pub(super) sugar: MonoSaccharide,
    pub(super) branches: Vec<PositionedGlycanStructure>,
    pub(super) inner_depth: usize,
    pub(super) outer_depth: usize,
    pub(super) branch: Vec<usize>,
}

impl Chemical for PositionedGlycanStructure {
    fn formula_inner(
        &self,
        sequence_index: SequencePosition,
        peptidoform_index: usize,
    ) -> MolecularFormula {
        self.sugar.formula_inner(sequence_index, peptidoform_index)
            + self
                .branches
                .iter()
                .map(|f| f.formula_inner(sequence_index, peptidoform_index))
                .sum::<MolecularFormula>()
    }
}

impl PositionedGlycanStructure {
    /// Generate all theoretical fragments for this glycan
    /// * `full_formula` the total formula of the whole peptide + glycan
    pub fn generate_theoretical_fragments(
        &self,
        model: &Model,
        peptidoform_ion_index: usize,
        peptidoform_index: usize,
        charge_carriers: &mut CachedCharge,
        full_formula: &Multi<MolecularFormula>,
        attachment: Option<(AminoAcid, usize)>,
    ) -> Vec<Fragment> {
        model
            .glycan
            .allow_structural
            .then(|| {
                // Get all base fragments from this node and all its children
                let mut base_fragments = self
                    .oxonium_fragments(peptidoform_ion_index, peptidoform_index, attachment)
                    .into_iter()
                    .flat_map(|f| {
                        f.with_charge_range(charge_carriers, model.glycan.oxonium_charge_range)
                    })
                    .flat_map(|f| f.with_neutral_losses(&model.glycan.neutral_losses))
                    .collect_vec();
                // Generate all Y fragments
                base_fragments.extend(
                    self.internal_break_points(peptidoform_index, attachment)
                        .iter()
                        .filter(|(_, bonds)| {
                            bonds.iter().all(|b| !matches!(b, GlycanBreakPos::B(_)))
                                && !bonds.iter().all(|b| matches!(b, GlycanBreakPos::End(_)))
                        })
                        .flat_map(move |(f, bonds)| {
                            full_formula.iter().map(move |full| {
                                Fragment::new(
                                    full - self.formula_inner(
                                        SequencePosition::default(),
                                        peptidoform_index,
                                    ) + f,
                                    Charge::zero(),
                                    peptidoform_ion_index,
                                    peptidoform_index,
                                    FragmentType::Y(
                                        bonds
                                            .iter()
                                            .filter(|b| !matches!(b, GlycanBreakPos::End(_)))
                                            .map(GlycanBreakPos::position)
                                            .cloned()
                                            .collect(),
                                    ),
                                )
                            })
                        })
                        .flat_map(|f| {
                            f.with_charge_range(charge_carriers, model.glycan.other_charge_range)
                        })
                        .flat_map(|f| f.with_neutral_losses(&model.glycan.neutral_losses)),
                );
                // Generate all diagnostic ions
                base_fragments.extend(
                    self.diagnostic_ions(peptidoform_ion_index, peptidoform_index, attachment)
                        .into_iter()
                        .flat_map(|f| {
                            f.with_charge_range(charge_carriers, model.glycan.oxonium_charge_range)
                        }),
                );
                base_fragments
            })
            .unwrap_or_default()
    }

    /// Get uncharged diagnostic ions from all positions
    fn diagnostic_ions(
        &self,
        peptidoform_ion_index: usize,
        peptidoform_index: usize,
        attachment: Option<(AminoAcid, usize)>,
    ) -> Vec<Fragment> {
        let mut output = self.sugar.diagnostic_ions(
            peptidoform_ion_index,
            peptidoform_index,
            crate::fragment::DiagnosticPosition::Glycan(
                self.position(attachment),
                self.sugar.clone(),
            ),
            true,
        );
        output.extend(
            self.branches.iter().flat_map(|b| {
                b.diagnostic_ions(peptidoform_ion_index, peptidoform_index, attachment)
            }),
        );

        output
    }

    /// Generate all fragments without charge and neutral loss options
    fn oxonium_fragments(
        &self,
        peptidoform_ion_index: usize,
        peptidoform_index: usize,
        attachment: Option<(AminoAcid, usize)>,
    ) -> Vec<Fragment> {
        // Generate the basic single breakage B fragments
        let mut base_fragments = vec![Fragment::new(
            self.formula_inner(SequencePosition::default(), peptidoform_index),
            Charge::zero(),
            peptidoform_ion_index,
            peptidoform_index,
            FragmentType::B(self.position(attachment)),
        )];
        // Extend with all internal fragments, meaning multiple breaking bonds
        base_fragments.extend(
            self.internal_break_points(peptidoform_index, attachment)
                .into_iter()
                .filter(|(_, breakages)| {
                    !breakages
                        .iter()
                        .all(|b| matches!(b, GlycanBreakPos::End(_)))
                })
                .filter(|(m, _)| *m != MolecularFormula::default())
                .map(|(m, b)| {
                    (
                        m,
                        [b, vec![GlycanBreakPos::B(self.position(attachment))]].concat(),
                    )
                })
                .map(|(formula, breakages)| {
                    Fragment::new(
                        formula,
                        Charge::zero(),
                        peptidoform_ion_index,
                        peptidoform_index,
                        FragmentType::Oxonium(breakages),
                    )
                }),
        );
        // Extend with the theoretical fragments for all branches of this position
        base_fragments.extend(self.branches.iter().flat_map(|b| {
            b.oxonium_fragments(peptidoform_ion_index, peptidoform_index, attachment)
        }));
        base_fragments
    }

    /// All possible bonds that can be broken and the molecular formula that would be held over if these bonds all broke and the broken off parts are lost.
    fn internal_break_points(
        &self,
        peptidoform_index: usize,
        attachment: Option<(AminoAcid, usize)>,
    ) -> Vec<(MolecularFormula, Vec<GlycanBreakPos>)> {
        // Find every internal fragment ending at this bond (in a B breakage) (all bonds found are Y breakages and endings)
        // Walk through all branches and determine all possible breakages
        if self.branches.is_empty() {
            vec![
                (
                    self.formula_inner(SequencePosition::default(), peptidoform_index),
                    vec![GlycanBreakPos::End(self.position(attachment))],
                ),
                (
                    MolecularFormula::default(),
                    vec![GlycanBreakPos::Y(self.position(attachment))],
                ),
            ]
        } else {
            self.branches
                .iter()
                .map(|b| b.internal_break_points(peptidoform_index, attachment)) // get all previous options
                .fold(Vec::new(), |accumulator, branch_options| {
                    if accumulator.is_empty() {
                        branch_options
                    } else {
                        let mut new_accumulator = Vec::new();
                        for base in &accumulator {
                            for option in &branch_options {
                                new_accumulator.push((
                                    &option.0 + &base.0,
                                    [option.1.clone(), base.1.clone()].concat(),
                                ));
                            }
                        }
                        new_accumulator
                    }
                })
                .into_iter()
                .map(|(m, b)| {
                    (
                        m + self
                            .sugar
                            .formula_inner(SequencePosition::default(), peptidoform_index),
                        b,
                    )
                })
                .chain(std::iter::once((
                    // add the option of it breaking here
                    MolecularFormula::default(),
                    vec![GlycanBreakPos::Y(self.position(attachment))],
                )))
                .collect()
        }
    }

    fn position(&self, attachment: Option<(AminoAcid, usize)>) -> GlycanPosition {
        GlycanPosition {
            inner_depth: self.inner_depth,
            series_number: self.outer_depth + 1,
            branch: self.branch.clone(),
            attachment,
        }
    }
}
