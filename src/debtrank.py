"""A clear, simplified implementation of the DebtRank contagion idea."""

import pandas as pd


def calculate_debtrank(network, shocked_bank):
    """Propagate distress after one bank fails and return its systemic impact.

    If a borrower is distressed, its lenders face losses.  For each lender,
    new distress equals the loss on its loan divided by its capital.  Distress
    is capped at 1.0, meaning the lender has exhausted all its capital.
    """
    if shocked_bank not in network:
        raise ValueError(f"{shocked_bank} is not in the lending network.")

    # h is each bank's total distress level: 0 means healthy, 1 means default.
    distress = {bank: 0.0 for bank in network.nodes}
    distress[shocked_bank] = 1.0

    # The value records the *new* distress to transmit in the next round.
    # Passing only the new amount avoids counting the same loss repeatedly.
    active_banks = {shocked_bank: 1.0}

    while active_banks:
        next_active_banks = {}

        for distressed_borrower, new_borrower_distress in active_banks.items():

            # In a lender -> borrower graph, predecessors are the lenders.
            for lender in network.predecessors(distressed_borrower):
                exposure = network[lender][distressed_borrower]["exposure"]
                lender_capital = network.nodes[lender]["capital"]

                # Calculate only the additional loss created in this round.
                additional_distress = (
                    new_borrower_distress * exposure / lender_capital
                )
                old_distress = distress[lender]
                new_distress = min(1.0, old_distress + additional_distress)

                if new_distress > old_distress:
                    distress[lender] = new_distress
                    # The next round transmits only this bank's new distress.
                    next_active_banks[lender] = (
                        next_active_banks.get(lender, 0.0)
                        + (new_distress - old_distress)
                    )

        active_banks = next_active_banks

    # Weight each bank's distress by its assets, then scale to 0-1.
    total_assets = sum(network.nodes[bank]["total_assets"] for bank in network.nodes)
    distressed_assets = sum(
        distress[bank] * network.nodes[bank]["total_assets"]
        for bank in network.nodes
    )
    systemic_impact = distressed_assets / total_assets

    return systemic_impact, distress


def rank_banks_by_systemic_impact(network):
    """Test every bank as the initial failure and return a sorted ranking."""
    results = []
    for bank in network.nodes:
        systemic_impact, _ = calculate_debtrank(network, bank)
        results.append({"bank_id": bank, "systemic_impact": systemic_impact})

    ranking = pd.DataFrame(results).sort_values(
        "systemic_impact", ascending=False
    )
    return ranking.reset_index(drop=True)
