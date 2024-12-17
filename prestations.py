def get_prestations():
    return {
        "droit_civil_contrats": {
            "label": "Droit civil et contrats",
            "prestations": {
                # CONSEIL ET ANALYSE
                "consultation_initiale": {
                    "label": "Consultation initiale",
                    "tarif": 200,
                    "definition": "Premier rendez-vous pour évaluer la situation juridique et définir les actions à entreprendre."
                },
                "consultation_juridique_et_reglementaire": {
                    "label": "Consultation juridique et réglementaire",
                    "tarif": 800,
                    "definition": "Analyse approfondie d'une situation juridique spécifique et conseil sur les implications réglementaires."
                },

                # RÉDACTION DE DOCUMENTS
                "redaction_conditions_generales": {
                    "label": "Rédaction des conditions générales",
                    "tarif": 800,
                    "definition": "Élaboration des termes et conditions régissant les relations entre une entreprise et ses clients."
                },
                "redaction_contrat_simple": {
                    "label": "Rédaction de contrat simple",
                    "tarif": 800,
                    "definition": "Élaboration d'un contrat standard couvrant les aspects essentiels d'un accord."
                },
                "redaction_contrat_complexe": {
                    "label": "Rédaction de contrat complexe",
                    "tarif": 2000,
                    "definition": "Préparation d'un contrat détaillé couvrant des situations juridiques complexes ou multiples."
                }
            }
        },
        "procédures_collectives": {
            "label": "procédures collectives",
            "prestations": {
                # PRÉVENTION ET ANTICIPATION
                "audit": {
                    "label": "Audit d'entreprise en difficulté",
                    "tarif": 1500,
                    "definition": "Audit d'une société en difficulté afin d'évaluer la pertinence d'une reprise. En général demandé par un acquéreur potentiel."
                },
                "procédure_sauvegarde": {
                    "label": "procédure de sauvegarde",
                    "tarif": 1500,
                    "definition": "Accompagnement d'une société en difficulté dans l'élaboration et la mise en oeuvre d'un plan de sauvegarde ou de mandat ad hoc. Pour les sociétés en difficulté qui ne sont pas en situation de cessation de paiement"
                },

                # PROCÉDURES DE TRAITEMENT DES DIFFICULTÉS
                "procédure_redressement": {
                    "label": "Procédure de redressement",
                    "tarif": 1000,
                    "definition": "Accompagnement d'une société en difficulté dans la mise en oeuvre d'un plan de redressement. Vallable pour les sociétés en situation de cessation de paiement dont la situation n'est pas irrémédiablement compromise"
                },
                "liquidation": {
                    "label": "Procédure de liquidation",
                    "tarif": 1000,
                    "definition": "Accompagnement d'une entreprise en situation de faillite dans le cadre d'une procédure de liquidation."
                },
                
                # CRÉANCIERS
                "déclaration_créance": {
                    "label": "Déclaration de créance",
                    "tarif": 800,
                    "definition": "Accompagnement juridique dans le cadre d'une procédure de déclaration de créance. Valable lorsqu'une entreprise est créancière d'une société en difficulté."
                }
            }
        },
        "droit_immobilier_commercial": {
            "label": "Droit immobilier et commercial",
            "prestations": {
                # RÉDACTION DE BAUX COMMERCIAUX
                "redaction_bail_commercial": {
                    "label": "Rédaction de bail commercial",
                    "tarif": 1500,
                    "definition": "Préparation d'un contrat de location pour un bien immobilier à usage commercial. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "redaction_bail_commercial_en_etat_futur_achevement_BEFA": {
                    "label": "Rédaction de bail commercial en état futur d'achèvement (BEFA)",
                    "tarif": 2500,
                    "definition": "Élaboration d'un bail pour un local commercial encore en construction ou en rénovation. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "redaction_bail_commercial_derogatoire": {
                    "label": "Rédaction de bail commercial dérogatoire",
                    "tarif": 1000,
                    "definition": "Préparation d'un bail commercial de courte durée, dérogeant au statut des baux commerciaux. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "redaction_bail_sous_location_commerciale": {
                    "label": "Rédaction de bail de sous-location à un bail commercial",
                    "tarif": 1000,
                    "definition": "Élaboration d'un contrat permettant à un locataire de louer tout ou partie du bien commercial à un tiers. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "redaction_bail_professionnel": {
                    "label": "Rédaction de bail professionnel",
                    "tarif": 800,
                    "definition": "Préparation d'un contrat de location pour un local destiné à l'exercice d'une profession libérale. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },

                # MODIFICATIONS ET RÉVISIONS
                "redaction_avenant_bail_commercial": {
                    "label": "Rédaction d'avenant à bail commercial",
                    "tarif": 500,
                    "definition": "Élaboration d'un document modifiant les termes d'un bail commercial existant. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "redaction_demande_revision_loyer": {
                    "label": "Rédaction de demande de révision de loyer",
                    "tarif": 500,
                    "definition": "Préparation d'une requête formelle pour ajuster le montant du loyer d'un bail commercial. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "redaction_demande_despecialisation": {
                    "label": "Rédaction de demande de déspécialisation",
                    "tarif": 400,
                    "definition": "Élaboration d'une demande pour modifier l'activité autorisée ou la destination dans un bail commercial. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },

                # RÉSILIATION ET RECOUVREMENT
                "procedure_resiliation_bail_commercial": {
                    "label": "Procédure de résiliation de bail commercial",
                    "tarif": 1500,
                    "definition": "Gestion juridique de la fin anticipée d'un bail commercial. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "redaction_commandement_clause_resolutoire": {
                    "label": "Rédaction de commandement visant la clause résolutoire",
                    "tarif": 400,
                    "definition": "Préparation d'un acte formel mettant en œuvre la clause de résiliation automatique du bail. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "mise_en_demeure_conflit_bail_commercial": {
                    "label": "Mise en demeure pour conflit de bail commercial",
                    "tarif": 400,
                    "definition": "Rédaction d'un avertissement formel dans le cadre d'un litige lié à un bail commercial. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "procedure_recouvrement_impayes": {
                    "label": "Procédure de recouvrement d'impayés",
                    "tarif": 500,
                    "definition": "Gestion juridique pour récupérer des loyers ou charges impayés dans le cadre d'un bail commercial. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },

                # RENOUVELLEMENT ET CESSION
                "redaction_conge": {
                    "label": "Rédaction de congé",
                    "tarif": 400,
                    "definition": "Préparation de l'acte mettant fin à un bail commercial à son terme. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "redaction_demande_renouvellement": {
                    "label": "Rédaction de demande de renouvellement",
                    "tarif": 400,
                    "definition": "Élaboration d'une requête formelle pour prolonger un bail commercial arrivant à échéance. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "redaction_cession_droit_bail": {
                    "label": "Rédaction de cession de droit au bail",
                    "tarif": 1500,
                    "definition": "Élaboration du contrat transférant les droits et obligations d'un bail commercial à un nouveau locataire. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },

                # PROCÉDURES JUDICIAIRES
                "procedure_juge_loyers_commerciaux": {
                    "label": "Procédure devant le juge des loyers commerciaux",
                    "tarif": 3000,
                    "definition": "Représentation juridique lors d'un litige porté devant un tribunal concernant le loyer d'un bail commercial. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "procedure_bail_commercial_tribunal_judiciaire_fond": {
                    "label": "Procédure de bail commercial devant le tribunal judiciaire (fond)",
                    "tarif": 2000,
                    "definition": "Représentation juridique dans un litige complexe lié à un bail commercial devant le tribunal. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "procedure_fixation_indemnite_eviction": {
                    "label": "Procédure de fixation d'indemnité d'éviction",
                    "tarif": 4000,
                    "definition": "Gestion juridique pour déterminer la compensation due au locataire en cas de non-renouvellement du bail. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },

                # AUTRES PROCÉDURES
                "purge_droit_preemption": {
                    "label": "Purge du droit de préemption",
                    "tarif": 500,
                    "definition": "Procédure visant à s'assurer qu'aucun tiers n'a de droit prioritaire d'achat sur un bien commercial. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },

                # CONSEIL ET ACCOMPAGNEMENT
                "consultation_juridique_et_reglementaire": {
                    "label": "Consultation juridique et réglementaire",
                    "tarif": 800,
                    "definition": "Analyse approfondie d'une situation juridique spécifique et conseil sur les implications réglementaires. Valable pour les professionnels, les personnes morales ou les particuliers se lançant dans l'entrepreneuriat"
                },
                "externalisation_service_immobilier_commercial": {
                    "label": "Externalisation juridique partielle",
                    "tarif": 2000,
                    "definition": "Accompagnement juridique sur des domaines spécifiques de l'entreprise, en complément des ressources internes existantes. Il s'agit d'externaliser une partie de l'équipe juridique d'une personne morale ou d'une société en matière d' ou d' commercial."
                }
            }
        },
        "droit_des_affaires": {
            "label": "Droit des affaires",
            "prestations": {
                # CRÉATION ET ORGANISATION
                "creation_entreprise": {
                    "label": "Création d'entreprise",
                    "tarif": 600,
                    "definition": "Accompagnement juridique complet pour la création d'une nouvelle entreprise."
                },
                "redaction_statuts_societe": {
                    "label": "Rédaction des statuts de société",
                    "tarif": 600,
                    "definition": "Élaboration du document juridique fondamental définissant la structure et le fonctionnement d'une société."
                },

                # OPÉRATIONS DE TRANSFORMATION
                "fusion_entreprises": {
                    "label": "Conseil en fusion d'entreprises",
                    "tarif": 5000,
                    "definition": "Assistance juridique pour les opérations de fusion d'entreprises."
                },
                "acquisition_entreprise": {
                    "label": "Conseil en acquisition d'entreprises",
                    "tarif": 2000,
                    "definition": "Assistance juridique pour les opérations de d'acquisition d'entreprises."
                },
                "cession_entreprise": {
                    "label": "Conseil en cession d'entreprises",
                    "tarif": 2000,
                    "definition": "Assistance juridique pour les opérations de cession d'entreprises."
                },

                # CONTRATS ET FONDS DE COMMERCE
                "location_gérance": {
                    "label": "Accompagnement en matière de location gérance",
                    "tarif": 2000,
                    "definition": "Assistance juridique pour les opérations de contractualisation d'une location gérance."
                },
                "acquisition_fonds_commerce": {
                    "label": "Acquisition d'un fonds de commerce",
                    "tarif": 1500,
                    "definition": "Accompagnement dans l'acquisition d'un fonds de commerce."
                },
                "contrats_commerciaux": {
                    "label": "Rédaction de contrats commerciaux",
                    "tarif": 1500,
                    "definition": "Élaboration de contrats commerciaux adaptés aux besoins spécifiques de l'entreprise."
                },
                "contentieux_commercial": {
                    "label": "Gestion de contentieux commercial",
                    "tarif": 2500,
                    "definition": "Représentation et défense des intérêts de l'entreprise dans les litiges commerciaux."
                },
                "externalisation_partielle": {
                    "label": "Externalisation juridique partielle",
                    "tarif": 2000,
                    "definition": "Accompagnement juridique sur des domaines spécifiques de l'entreprise, en complément des ressources internes existantes. Il s'agit d'externaliser une partie de l'équipe juridique d'une personne morale ou d'une société en matière de droit des affaires."
                }
            }
        },
        
        "droit_de_la_propriete_intellectuelle": {
            "label": "Droit de la propriété intellectuelle",
            "prestations": {
                # PROTECTION DES DROITS
                "depot_marque": {
                    "label": "Dépôt de marque",
                    "tarif": 1000,
                    "definition": "Procédure juridique pour protéger une marque commerciale auprès des autorités compétentes."
                },
                "depot_brevet": {
                    "label": "Dépôt de brevet",
                    "tarif": 3000,
                    "definition": "Assistance dans la procédure de dépôt d'un brevet pour protéger une invention."
                },
                "protection_droit_auteur": {
                    "label": "Protection des droits d'auteur",
                    "tarif": 1500,
                    "definition": "Conseil et assistance pour la protection des œuvres intellectuelles et artistiques."
                },

                # CONTRATS ET EXPLOITATION
                "contrat_licence": {
                    "label": "Rédaction de contrat de licence",
                    "tarif": 2000,
                    "definition": "Élaboration d'un contrat pour l'exploitation d'une propriété intellectuelle."
                },

                # CONTENTIEUX ET DÉFENSE
                "contentieux_contrefacon": {
                    "label": "Contentieux en contrefaçon",
                    "tarif": 3500,
                    "definition": "Représentation juridique dans les litiges liés à la contrefaçon de propriété intellectuelle."
                },

                # ACCOMPAGNEMENT GLOBAL
                "externalisation_partielle": {
                    "label": "Externalisation juridique partielle",
                    "tarif": 2000,
                    "definition": "Accompagnement juridique sur des domaines spécifiques de l'entreprise, en complément des ressources internes existantes. Il s'agit d'externaliser une partie de l'équipe juridique d'une personne morale ou d'une société en matière de propriété intellectuelle."
                }
            }
        },

        "droit_du_travail": {
            "label": "Droit du travail",
            "prestations": {
                # CONSEIL ET CONSULTATION
                "consultation_juridique_et_reglementaire": {
                    "label": "Consultation juridique et réglementaire en droit du travail",
                    "tarif": 300,
                    "definition": "Analyse approfondie d'une situation spécifique en droit du travail et conseil sur les implications réglementaires."
                },
                "conseil_licenciement": {
                    "label": "Conseil en procédure de licenciement",
                    "tarif": 600,
                    "definition": "Accompagnement et conseil pour la mise en place d'une procédure de licenciement conforme au droit du travail."
                },

                # RÉDACTION DE CONTRATS
                "redaction_contrat_travail": {
                    "label": "Rédaction de contrat de travail salarié",
                    "tarif": 500,
                    "definition": "Élaboration d'un contrat de travail personnalisé pour un salarié sans responsabilités particulières et sans management."
                },
                "redaction_contrat_travail_cadre": {
                    "label": "Rédaction de contrat de travail pour un cadre",
                    "tarif": 1200,
                    "definition": "Élaboration d'un contrat de travail personnalisé pour un poste à responsabilités du type cadre ou cadre supérieur. Il convient pour les métiers qui présentent un degre de responsabilité plus important qu'un simple salarié."
                },
                "redaction_contrat_travail_dirigeant": {
                    "label": "Rédaction de contrat de travail pour un dirigeant",
                    "tarif": 2500,
                    "definition": "Élaboration d'un contrat de travail personnalisé pour un cadre supérieur, un membre de codir ou comex ou un dirigeant et conforme à la législation en vigueur."
                },

                # NÉGOCIATIONS ET RUPTURES
                "negociation_rupture_conventionnelle": {
                    "label": "Négociation de rupture conventionnelle",
                    "tarif": 800,
                    "definition": "Assistance et conseil dans le processus de négociation d'une rupture conventionnelle."
                },

                # PROCÉDURES COLLECTIVES
                "Plan_sauvegarde_emploi": {
                    "label": "Elaboration d'un plan de sauvegarde de l'emploi",
                    "tarif": 3000,
                    "definition": "Elaboration d'un PSE, plan de sauvegarde de l'emploi, destiné à encadrer la procédure de licenciement de plusieurs salariés à la fois par l'entreprise pour un motif économique. Cette prestation intègre les livres 1 et 2."
                },

                # DOCUMENTS D'ENTREPRISE
                "règlement_intérieur": {
                    "label": "Rédaction ou révision d'un règlement intérieur",
                    "tarif": 1000,
                    "definition": "Élaboration ou révision d'un règlement intérieur."
                },
                "redaction_accord_collectif": {
                    "label": "Rédaction d'un accord collectif",
                    "tarif": 2500,
                    "definition": "Élaboration d'un accord collectif et négociation avec le CSE."
                },

                # CONTENTIEUX
                "representation_en_justice": {
                    "label": "Représentation en justice pour litige de droit du travail",
                    "tarif": 2000,
                    "definition": "Représentation et défense des intérêts du client devant les tribunaux pour un litige lié au droit du travail."
                },

                # ACCOMPAGNEMENT GLOBAL
                "externalisation_partielle": {
                    "label": "Externalisation juridique partielle",
                    "tarif": 2000,
                    "definition": "Accompagnement juridique sur des domaines spécifiques de l'entreprise, en complément des ressources internes existantes. Il s'agit d'externaliser une partie de l'équipe juridique d'une personne morale ou d'une société en matière de droit du travail."
                }
            }
        },

        "droit_de_la_construction": {
            "label": "Droit de la construction",
            "prestations": {
                # CONTRATS ET CONSEIL
                "redaction_contrat_construction": {
                    "label": "Rédaction de contrat de construction",
                    "tarif": 2500,
                    "definition": "Élaboration d'un contrat détaillé pour un projet de construction, incluant les spécifications techniques et les conditions juridiques."
                },
                "conseil_maitrise_ouvrage": {
                    "label": "Conseil en maîtrise d'ouvrage",
                    "tarif": 1800,
                    "definition": "Assistance juridique au maître d'ouvrage tout au long du projet de construction."
                },
                "conseil_contrats_sous_traitance": {
                    "label": "Conseil en contrats de sous-traitance",
                    "tarif": 1600,
                    "definition": "Élaboration et révision de contrats de sous-traitance dans le domaine de la construction."
                },

                # GESTION DES TRAVAUX
                "assistance_reception_travaux": {
                    "label": "Assistance à la réception des travaux",
                    "tarif": 1500,
                    "definition": "Conseil juridique lors de la phase de réception des travaux, y compris la gestion des réserves."
                },
                "audit_juridique_chantier": {
                    "label": "Audit juridique de chantier",
                    "tarif": 2500,
                    "definition": "Évaluation complète de la conformité juridique d'un chantier de construction."
                },

                # CONTENTIEUX ET LITIGES
                "gestion_litiges_construction": {
                    "label": "Gestion des litiges de construction",
                    "tarif": 3000,
                    "definition": "Représentation juridique dans les conflits liés à la construction (malfaçons, retards, etc.)."
                },
                "contentieux_assurance_construction": {
                    "label": "Contentieux en assurance construction",
                    "tarif": 2800,
                    "definition": "Gestion des litiges impliquant les assurances dans le cadre de projets de construction."
                },
                "gestion_responsabilite_constructeurs": {
                    "label": "Gestion de la responsabilité des constructeurs",
                    "tarif": 2200,
                    "definition": "Traitement des questions de responsabilité des différents intervenants dans un projet de construction."
                },

                # AUTORISATIONS ET PERMIS
                "conseil_permis_construire": {
                    "label": "Conseil en permis de construire",
                    "tarif": 1200,
                    "definition": "Assistance dans l'obtention ou la contestation de permis de construire."
                },

                # RÉSOLUTION AMIABLE
                "mediation_construction": {
                    "label": "Médiation en droit de la construction",
                    "tarif": 1800,
                    "definition": "Conduite de médiations pour résoudre les conflits liés à la construction hors des tribunaux."
                },

                # ACCOMPAGNEMENT GLOBAL
                "externalisation_partielle": {
                    "label": "Externalisation juridique partielle",
                    "tarif": 2000,
                    "definition": "Accompagnement juridique sur des domaines spécifiques de l'entreprise, en complément des ressources internes existantes. Il s'agit d'externaliser une partie de l'équipe juridique d'une personne morale ou d'une société en matière de droit de la construction."
                }
            }
        },

        "droit_de_la_famille": {
            "label": "Droit de la famille",
            "prestations": {
                # DIVORCE
                "procedure_divorce_contentieux": {
                    "label": "Procédure de divorce contentieux",
                    "tarif": 2000,
                    "definition": "Gestion juridique d'une procédure de divorce non consensuelle."
                },
                "procedure_divorce_amiable": {
                    "label": "Procédure de divorce amiable",
                    "tarif": 1500,
                    "definition": "Accompagnement juridique pour un divorce par consentement mutuel."
                },

                # ENFANTS ET FAMILLE
                "garde_enfants": {
                    "label": "Litige sur la garde des enfants",
                    "tarif": 2000,
                    "definition": "Représentation dans un conflit concernant la garde des enfants."
                },
                "pension_alimentaire": {
                    "label": "Fixation/révision de pension alimentaire",
                    "tarif": 1000,
                    "definition": "Procédure pour établir ou modifier le montant d'une pension alimentaire."
                },
                "adoption": {
                    "label": "Procédure d'adoption",
                    "tarif": 3000,
                    "definition": "Accompagnement juridique dans le processus d'adoption d'un enfant."
                },

                # SUCCESSIONS ET PATRIMOINE
                "consultation_succession": {
                    "label": "Consultation en matière de succession",
                    "tarif": 600,
                    "definition": "Consultation sur un sujet de succession en dehors d'une procédure contentieuse."
                },
                "succession": {
                    "label": "Règlement de succession",
                    "tarif": 2500,
                    "definition": "Assistance juridique pour le règlement d'une succession."
                },

                # RÉGIMES MATRIMONIAUX
                "redaction_contrat_mariage": {
                    "label": "Rédaction de contrat de mariage",
                    "tarif": 1500,
                    "definition": "Élaboration d'un contrat de mariage adapté à la situation des futurs époux."
                },
                "procedure_changement_regime_matrimonial": {
                    "label": "Procédure de changement de régime matrimonial",
                    "tarif": 2000,
                    "definition": "Assistance juridique pour modifier le régime matrimonial d'un couple marié."
                },

                # PROTECTION DES PERSONNES
                "protection_majeur_vulnerable": {
                    "label": "Protection d'un majeur vulnérable",
                    "tarif": 1800,
                    "definition": "Mise en place de mesures de protection juridique pour un adulte vulnérable (tutelle, curatelle)."
                },

                # FILIATION
                "contestation_paternite": {
                    "label": "Contestation ou recherche de paternité",
                    "tarif": 2200,
                    "definition": "Procédure juridique pour contester ou établir la paternité d'un enfant."
                },

                # RÉSOLUTION AMIABLE
                "mediation_familiale": {
                    "label": "Médiation familiale",
                    "tarif": 1200,
                    "definition": "Conduite de séances de médiation pour résoudre les conflits familiaux à l'amiable."
                }
            }
        },

        "droit_penal": {
            "label": "Droit pénal",
            "prestations": {
                # ASSISTANCE IMMÉDIATE
                "assistance_garde_vue": {
                    "label": "Assistance en garde à vue",
                    "tarif": 800,
                    "definition": "Assistance juridique d'un client placé en garde à vue."
                },
                "conseil_enquete_preliminaire": {
                    "label": "Conseil lors d'une enquête préliminaire",
                    "tarif": 1200,
                    "definition": "Accompagnement juridique durant la phase d'enquête préliminaire."
                },

                # DÉFENSE PÉNALE
                "defense_penale": {
                    "label": "Défense pénale",
                    "tarif": 2500,
                    "definition": "Représentation et défense d'un client accusé d'une infraction pénale."
                },
                "recours_detention_provisoire": {
                    "label": "Recours contre une détention provisoire",
                    "tarif": 2000,
                    "definition": "Procédure visant à contester une décision de placement en détention provisoire."
                },

                # VICTIMES
                "constitution_partie_civile": {
                    "label": "Constitution de partie civile",
                    "tarif": 1500,
                    "definition": "Assistance juridique pour se constituer partie civile dans une affaire pénale."
                }
            }
        },

        "droit_de_la_consommation": {
            "label": "Droit de la consommation",
            "prestations": {
                # CONSEIL AUX PROFESSIONNELS
                "conseil_pratiques_commerciales": {
                    "label": "Conseil en pratiques commerciales",
                    "tarif": 1200,
                    "definition": "Avis juridique sur la conformité des pratiques commerciales avec le droit de la consommation."
                },
                "redaction_cgv": {
                    "label": "Rédaction de conditions générales de vente",
                    "tarif": 1000,
                    "definition": "Élaboration de CGV conformes au droit de la consommation."
                },
                "conseil_etiquetage": {
                    "label": "Conseil en étiquetage et information",
                    "tarif": 900,
                    "definition": "Assistance juridique pour la conformité de l'étiquetage et de l'information des consommateurs."
                },
                "conseil_vente_distance": {
                    "label": "Conseil en vente à distance",
                    "tarif": 1100,
                    "definition": "Assistance juridique pour la conformité des ventes en ligne et à distance."
                },

                # LITIGES ET CONTENTIEUX
                "litige_consommation": {
                    "label": "Litige de consommation",
                    "tarif": 800,
                    "definition": "Représentation dans les litiges entre consommateurs et professionnels."
                },
                "contentieux_garanties": {
                    "label": "Contentieux des garanties",
                    "tarif": 1500,
                    "definition": "Gestion des litiges liés aux garanties légales et commerciales."
                },
                "action_groupe": {
                    "label": "Action de groupe",
                    "tarif": 3000,
                    "definition": "Organisation et conduite d'une action de groupe pour les consommateurs."
                },

                # CONFORMITÉ ET FORMATION
                "audit_conformite_consommation": {
                    "label": "Audit de conformité en droit de la consommation",
                    "tarif": 2500,
                    "definition": "Évaluation complète de la conformité d'une entreprise au droit de la consommation."
                },
                "formation_droit_consommation": {
                    "label": "Formation en droit de la consommation",
                    "tarif": 1800,
                    "definition": "Sessions de formation pour les professionnels sur le droit de la consommation."
                },

                # RÉSOLUTION AMIABLE
                "mediation_consommation": {
                    "label": "Médiation de la consommation",
                    "tarif": 1000,
                    "definition": "Conduite de médiations entre consommateurs et professionnels."
                }
            }
        },

        "droit_de_la_sante": {
            "label": "Droit de la santé",
            "prestations": {
                # RESPONSABILITÉ ET LITIGES
                "responsabilite_medicale": {
                    "label": "Responsabilité médicale",
                    "tarif": 2500,
                    "definition": "Gestion des litiges liés à la responsabilité des professionnels de santé."
                },
                "contentieux_securite_sociale": {
                    "label": "Contentieux de la sécurité sociale",
                    "tarif": 1800,
                    "definition": "Gestion des litiges avec les organismes de sécurité sociale."
                },
                "contentieux_ordres_professionnels": {
                    "label": "Contentieux des ordres professionnels",
                    "tarif": 2200,
                    "definition": "Représentation devant les instances ordinales des professions de santé."
                },

                # DROITS DES PATIENTS
                "droit_patients": {
                    "label": "Droit des patients",
                    "tarif": 1200,
                    "definition": "Conseil et représentation des patients dans l'exercice de leurs droits."
                },
                "contentieux_handicap": {
                    "label": "Contentieux du handicap",
                    "tarif": 1700,
                    "definition": "Gestion des litiges liés aux droits des personnes handicapées."
                },

                # CONSEIL AUX ÉTABLISSEMENTS
                "conseil_etablissements_sante": {
                    "label": "Conseil aux établissements de santé",
                    "tarif": 2000,
                    "definition": "Assistance juridique pour les hôpitaux et cliniques."
                },
                "droit_pharmacie": {
                    "label": "Droit de la pharmacie",
                    "tarif": 1900,
                    "definition": "Conseil juridique spécifique au secteur pharmaceutique."
                },

                # RECHERCHE ET INNOVATION
                "conseil_recherche_biomedicale": {
                    "label": "Conseil en recherche biomédicale",
                    "tarif": 2800,
                    "definition": "Assistance juridique pour les projets de recherche en santé."
                },
                "droit_bioethique": {
                    "label": "Droit de la bioéthique",
                    "tarif": 2500,
                    "definition": "Conseil sur les questions éthiques et juridiques en matière de bioéthique."
                },

                # PROTECTION DES DONNÉES
                "protection_donnees_sante": {
                    "label": "Protection des données de santé",
                    "tarif": 2100,
                    "definition": "Conseil sur la conformité RGPD dans le secteur de la santé."
                }
            }
        },

        "droit_nouvelles_technologies": {
            "label": "Droit des nouvelles technologies",
            "prestations": {
                # PROTECTION DES DONNÉES
                "protection_donnees_personnelles": {
                    "label": "Protection des données personnelles",
                    "tarif": 2200,
                    "definition": "Conseil et mise en conformité RGPD."
                },
                "cybersecurite": {
                    "label": "Cybersécurité",
                    "tarif": 2800,
                    "definition": "Conseil juridique en matière de sécurité informatique."
                },

                # CONTRATS IT
                "contrats_informatiques": {
                    "label": "Contrats informatiques",
                    "tarif": 1800,
                    "definition": "Rédaction et négociation de contrats IT."
                },
                "contrats_cloud": {
                    "label": "Contrats cloud",
                    "tarif": 2100,
                    "definition": "Négociation et rédaction de contrats de services cloud."
                },

                # E-COMMERCE ET INTERNET
                "contentieux_internet": {
                    "label": "Contentieux internet",
                    "tarif": 2500,
                    "definition": "Gestion des litiges liés à l'utilisation d'internet."
                },
                "conseil_commerce_electronique": {
                    "label": "Conseil en commerce électronique",
                    "tarif": 1900,
                    "definition": "Assistance juridique pour les activités de e-commerce."
                },
                "conformite_sites_web": {
                    "label": "Conformité des sites web",
                    "tarif": 1500,
                    "definition": "Audit et conseil pour la conformité légale des sites web."
                },

                # PROPRIÉTÉ INTELLECTUELLE
                "propriete_intellectuelle_numerique": {
                    "label": "Propriété intellectuelle numérique",
                    "tarif": 2000,
                    "definition": "Protection des droits de propriété intellectuelle dans l'environnement numérique."
                },

                # RÉGLEMENTATIONS SPÉCIFIQUES
                "reglementation_telecoms": {
                    "label": "Réglementation des télécommunications",
                    "tarif": 2300,
                    "definition": "Conseil sur la réglementation des télécommunications."
                },
                "reglementation_ia": {
                    "label": "Réglementation de l'intelligence artificielle",
                    "tarif": 3000,
                    "definition": "Conseil sur les aspects juridiques de l'IA."
                }
            }
        }
        "droit_bancaire_financier": {
            "label": "Droit bancaire et financier",
            "prestations": {
                # CONTENTIEUX ET LITIGES
                "contentieux_bancaire": {
                    "label": "Contentieux bancaire",
                    "tarif": 2500,
                    "definition": "Gestion des litiges entre banques et clients."
                },
                "contentieux_financier": {
                    "label": "Contentieux financier", 
                    "tarif": 3000,
                    "definition": "Représentation dans les litiges financiers complexes."
                },

                # CONFORMITÉ ET RÉGLEMENTATION
                "reglementation_bancaire": {
                    "label": "Réglementation bancaire",
                    "tarif": 3000,
                    "definition": "Conseil sur la conformité aux réglementations bancaires."
                },
                "reglementation_assurance": {
                    "label": "Réglementation des assurances",
                    "tarif": 2400,
                    "definition": "Conseil sur la conformité aux réglementations des assurances."
                },
                "lutte_blanchiment": {
                    "label": "Lutte contre le blanchiment",
                    "tarif": 3200,
                    "definition": "Mise en place de procédures anti-blanchiment."
                },
                "audit_conformite_bancaire": {
                    "label": "Audit de conformité bancaire",
                    "tarif": 3800,
                    "definition": "Évaluation complète de la conformité d'un établissement bancaire."
                },

                # CONTRATS ET OPÉRATIONS
                "contrats_financiers": {
                    "label": "Contrats financiers",
                    "tarif": 2200,
                    "definition": "Rédaction et négociation de contrats financiers complexes."
                },
                "conseil_operations_bourse": {
                    "label": "Conseil en opérations de bourse",
                    "tarif": 2800,
                    "definition": "Assistance juridique pour les opérations sur les marchés financiers."
                },
                "financement_projet": {
                    "label": "Financement de projet",
                    "tarif": 3500,
                    "definition": "Structuration juridique de financements de projets."
                },

                # INNOVATION FINANCIÈRE
                "conseil_fintechs": {
                    "label": "Conseil aux fintechs",
                    "tarif": 2600,
                    "definition": "Assistance juridique spécifique aux entreprises fintech."
                }
            }
        },

        "droit_associations_fondations": {
            "label": "Droit des associations et des fondations",
            "prestations": {
                # CRÉATION ET STRUCTURATION
                "creation_association": {
                    "label": "Création d'association",
                    "tarif": 800,
                    "definition": "Assistance juridique pour la création d'une association."
                },
                "creation_fonds_dotation": {
                    "label": "Création de fonds de dotation",
                    "tarif": 2500,
                    "definition": "Assistance juridique pour la création d'un fonds de dotation."
                },
                "creation_fondation": {
                    "label": "Création de fondation",
                    "tarif": 2500,
                    "definition": "Assistance juridique pour la création d'une fondation."
                },
                "redaction_statuts": {
                    "label": "Rédaction de statuts",
                    "tarif": 1000,
                    "definition": "Élaboration des statuts d'associations ou de fondations."
                },

                # GOUVERNANCE ET GESTION
                "conseil_gouvernance": {
                    "label": "Conseil en gouvernance",
                    "tarif": 1500,
                    "definition": "Conseil sur les bonnes pratiques de gouvernance d'une fondation, d'un fonds de dotation ou d'une association."
                },
                "fiscalite_associations": {
                    "label": "Fiscalité des associations",
                    "tarif": 1200,
                    "definition": "Conseil sur les aspects fiscaux spécifiques aux associations."
                },

                # FINANCEMENT ET RESSOURCES
                "mecenat_sponsoring": {
                    "label": "Mécénat et sponsoring",
                    "tarif": 1800,
                    "definition": "Conseil juridique sur les opérations de mécénat et de sponsoring."
                },
                "conseil_dons_legs": {
                    "label": "Conseil en dons et legs",
                    "tarif": 1400,
                    "definition": "Assistance juridique pour la gestion des dons et legs."
                },

                # ÉVOLUTION ET TRANSFORMATION
                "fusion_association": {
                    "label": "Fusion d'associations",
                    "tarif": 2000,
                    "definition": "Accompagnement juridique dans le processus de fusion d'associations."
                },
                "transformation_association": {
                    "label": "Transformation d'association",
                    "tarif": 1600,
                    "definition": "Assistance juridique pour la transformation d'une association (ex: en fondation)."
                },

                # CONTENTIEUX
                "contentieux_associatif": {
                    "label": "Contentieux associatif",
                    "tarif": 1700,
                    "definition": "Gestion des litiges impliquant des associations."
                }
            }
        },

        "droit_des_societes": {
            "label": "Droit des sociétés",
            "prestations": {
                # CRÉATION ET VIE COURANTE
                "creation_societe": {
                    "label": "Création de société",
                    "tarif": 600,
                    "definition": "Assistance juridique pour la création d'une société commerciale."
                },
                "secretariat_juridique": {
                    "label": "Secrétariat juridique",
                    "tarif": 1000,
                    "definition": "Gestion des formalités juridiques courantes des sociétés."
                },
                "modification_statuts": {
                    "label": "Modification de statuts",
                    "tarif": 800,
                    "definition": "Rédaction et formalités de modification des statuts."
                },

                # OPÉRATIONS DE TRANSFORMATION
                "fusion_acquisition": {
                    "label": "Fusion-acquisition",
                    "tarif": 5000,
                    "definition": "Accompagnement juridique dans les opérations de fusion ou d'acquisition."
                },
                "transmission_entreprise": {
                    "label": "Transmission d'entreprise",
                    "tarif": 3500,
                    "definition": "Conseil juridique pour la transmission d'entreprise."
                },
                "restructuration_societe": {
                    "label": "Restructuration de société",
                    "tarif": 4000,
                    "definition": "Assistance juridique dans les opérations de restructuration."
                },

                # GOUVERNANCE ET RELATIONS INTERNES
                "pacte_actionnaires": {
                    "label": "Pacte d'actionnaires",
                    "tarif": 2000,
                    "definition": "Rédaction de pactes d'actionnaires."
                },
                "conseil_gouvernance_entreprise": {
                    "label": "Conseil en gouvernance d'entreprise",
                    "tarif": 2800,
                    "definition": "Conseil sur les meilleures pratiques de gouvernance d'entreprise."
                },

                # AUDIT ET CONTENTIEUX
                "audit_juridique": {
                    "label": "Audit juridique",
                    "tarif": 3000,
                    "definition": "Réalisation d'un audit juridique complet de la société."
                },
                "contentieux_societaire": {
                    "label": "Contentieux sociétaire",
                    "tarif": 2500,
                    "definition": "Gestion des litiges entre associés ou avec la société."
                },

                # ACCOMPAGNEMENT GLOBAL
                "externalisation_partielle": {
                    "label": "Externalisation juridique partielle",
                    "tarif": 2000,
                    "definition": "Accompagnement juridique sur des domaines spécifiques de l'entreprise, en complément des ressources internes existantes."
                }
            }
        },

        "droit_de_la_distribution": {
            "label": "Droit de la distribution",
            "prestations": {
                # CONTRATS DE DISTRIBUTION
                "redaction_contrat_distribution": {
                    "label": "Rédaction de contrat de distribution",
                    "tarif": 2000,
                    "definition": "Élaboration de contrats de distribution adaptés."
                },
                "concession_commerciale": {
                    "label": "Concession commerciale",
                    "tarif": 2200,
                    "definition": "Conseil et rédaction de contrats de concession commerciale."
                },
                "agence_commerciale": {
                    "label": "Agence commerciale",
                    "tarif": 1800,
                    "definition": "Conseil et rédaction de contrats d'agence commerciale."
                },

                # RÉSEAUX ET FRANCHISE
                "franchise": {
                    "label": "Conseil en franchise",
                    "tarif": 2500,
                    "definition": "Assistance juridique pour la mise en place et la gestion de réseaux de franchise."
                },
                "distribution_selective": {
                    "label": "Distribution sélective",
                    "tarif": 2300,
                    "definition": "Mise en place de systèmes de distribution sélective conformes au droit."
                },
                "distribution_en_ligne": {
                    "label": "Distribution en ligne",
                    "tarif": 2100,
                    "definition": "Conseil juridique pour la distribution via internet."
                },

                # CONTENTIEUX ET RUPTURE
                "contentieux_distribution": {
                    "label": "Contentieux de la distribution",
                    "tarif": 3000,
                    "definition": "Gestion des litiges liés aux contrats de distribution."
                },
                "rupture_relations_commerciales": {
                    "label": "Rupture de relations commerciales",
                    "tarif": 2400,
                    "definition": "Gestion juridique de la rupture de relations commerciales établies."
                },

                # CONCURRENCE ET AUDIT
                "pratiques_restrictives": {
                    "label": "Pratiques restrictives de concurrence",
                    "tarif": 2700,
                    "definition": "Conseil et contentieux relatifs aux pratiques restrictives de concurrence."
                },
                "audit_reseau_distribution": {
                    "label": "Audit de réseau de distribution",
                    "tarif": 3500,
                    "definition": "Évaluation complète de la conformité juridique d'un réseau de distribution."
                },

                # ACCOMPAGNEMENT GLOBAL
                "externalisation_partielle": {
                    "label": "Externalisation juridique partielle",
                    "tarif": 2000,
                    "definition": "Accompagnement juridique sur des domaines spécifiques de l'entreprise, en complément des ressources internes existantes."
                }
            }
        }


        
def get_prestations():
    return {
        "droit_administratif": {
            "label": "Droit administratif",
            "prestations": {
                # CONTENTIEUX ET RESPONSABILITÉ
                "contentieux_administratif": {
                    "label": "Contentieux administratif",
                    "tarif": 2500,
                    "definition": "Représentation devant les juridictions administratives."
                },
                "responsabilite_administrative": {
                    "label": "Responsabilité administrative",
                    "tarif": 2400,
                    "definition": "Gestion des litiges liés à la responsabilité de l'administration."
                },
                "contentieux_fiscal": {
                    "label": "Contentieux fiscal",
                    "tarif": 3000,
                    "definition": "Gestion des litiges avec l'administration fiscale."
                },

                # CONSEIL AUX COLLECTIVITÉS 
                "conseil_collectivites_territoriales": {
                    "label": "Conseil aux collectivités territoriales",
                    "tarif": 2300,
                    "definition": "Assistance juridique aux collectivités locales."
                },
                "conseil_marches_publics": {
                    "label": "Conseil en marchés publics",
                    "tarif": 2200,
                    "definition": "Assistance juridique dans les procédures de marchés publics."
                },

                # URBANISME ET ENVIRONNEMENT
                "urbanisme_amenagement": {
                    "label": "Urbanisme et aménagement",
                    "tarif": 2800,
                    "definition": "Conseil en droit de l'urbanisme et de l'aménagement du territoire."
                },
                "droit_environnement": {
                    "label": "Droit de l'environnement",
                    "tarif": 2600,
                    "definition": "Conseil et contentieux en droit de l'environnement."
                },

                # FONCTION PUBLIQUE ET DOMAINE PUBLIC
                "fonction_publique": {
                    "label": "Droit de la fonction publique",
                    "tarif": 2000,
                    "definition": "Conseil et contentieux relatifs au statut des fonctionnaires."
                },
                "domaine_public": {
                    "label": "Droit du domaine public",
                    "tarif": 2100,
                    "definition": "Conseil sur l'utilisation et la gestion du domaine public."
                },

                # DROIT DES ÉTRANGERS
                "contentieux_etrangers": {
                    "label": "Contentieux des étrangers",
                    "tarif": 1900,
                    "definition": "Gestion des litiges liés au droit des étrangers, autorisation de séjour, OQTF, etc."
                }
            }
        },

        "droit_de_l'immobilier": {
            "label": "Droit de l'immobilier",
            "prestations": {
                # LITIGES D'ACHAT ET VENTE
                "litiges_vente_immobiliere": {
                    "label": "Litiges en vente immobilière",
                    "tarif": 1200,
                    "definition": "Assistance juridique pour tous les litiges liés à l'achat ou la vente d'un bien immobilier : vices cachés, non-conformité, problèmes liés à la garantie décennale, manquement à l'obligation d'information du vendeur, problèmes de diagnostic immobilier, défaut de surface Carrez, etc. Vaut pour les situations ou le bien est un bien à usage d'habitation."
                },

                # LITIGES LOCATIFS
                "litige_location_immobiliere": {
                    "label": "Litiges locatifs",
                    "tarif": 1500,
                    "definition": "Assistance juridique pour les conflits entre propriétaires et locataires : impayés de loyer, non-respect du bail, problèmes d'entretien courant, dépôt de garantie, état des lieux, charges locatives, etc. Pour biens à usage d'habitation uniquement."
                },
                "expulsion_location_immobiliere": {
                    "label": "Procédure d'expulsion locative",
                    "tarif": 1500,
                    "definition": "Gestion des litiges locatifs divers et des loyers impayés. Concerne en général un propriétaire de bien immobilier."
                },

                # COPROPRIÉTÉ ET VOISINAGE
                "droit_copropriete": {
                    "label": "Droit de la copropriété",
                    "tarif": 2000,
                    "definition": "Gestion des litiges et conseil en droit de la copropriété. Concerne en général pour les particuliers."
                },
                "trouble_anormal_voisinage": {
                    "label": "Trouble anormal de voisinage",
                    "tarif": 1500,
                    "definition": "Gestion des litiges entre voisins en raison de nuisances ou de bruit anormaux."
                },

                # PROPRIÉTÉ ET EXPERTISE
                "droit_de_la_propriete": {
                    "label": "Droit de la propriété",
                    "tarif": 2200,
                    "definition": "Assistance juridique en matière de litiges ayant pour origine le non respect de la propriété privée. Concerne en général pour les particuliers."
                },
                "accompagnement_expertise_judiciaire": {
                    "label": "Accompagnement expertise judiciaire",
                    "tarif": 2500,
                    "definition": "Accompagnement et défense dans le cadre d'une procédure d'expertise judiciaire."
                },

                # CRÉATION DE SOCIÉTÉ
                "creation_societe_civile_immobiliere": {
                    "label": "Création de SCI",
                    "tarif": 1000,
                    "definition": "Accompagnement dans la création et la rédaction des statuts d'une société civile immobilière (SCI)."
                }
            }
        },

        "compliance": {
            "label": "Compliance et Conformité",
            "prestations": {
                # ANTICORRUPTION ET ÉTHIQUE
                "programme_anticorruption": {
                    "label": "Programme anticorruption",
                    "tarif": 5000,
                    "definition": "Élaboration et mise en place d'un programme de conformité anticorruption complet (Loi Sapin II)."
                },
                "code_ethique": {
                    "label": "Élaboration de code éthique",
                    "tarif": 3000,
                    "definition": "Rédaction d'un code éthique et de conduite adapté à l'entreprise."
                },

                # PROTECTION DES DONNÉES
                "audit_conformite_rgpd": {
                    "label": "Audit de conformité RGPD",
                    "tarif": 3500,
                    "definition": "Évaluation complète de la conformité au Règlement Général sur la Protection des Données."
                },
                "mise_en_place_rgpd": {
                    "label": "Mise en place RGPD",
                    "tarif": 4500,
                    "definition": "Assistance à la mise en conformité RGPD, incluant la rédaction de politiques et procédures."
                },

                # AUDITS ET ÉVALUATION
                "cartographie_risques": {
                    "label": "Cartographie des risques",
                    "tarif": 4000,
                    "definition": "Identification et évaluation des risques de conformité au sein de l'entreprise."
                },
                "audit_tiers": {
                    "label": "Audit de conformité des tiers",
                    "tarif": 4000,
                    "definition": "Évaluation de la conformité des partenaires commerciaux et fournisseurs."
                },

                # PROGRAMMES SPÉCIFIQUES
                "plan_devoir_vigilance": {
                    "label": "Plan de devoir de vigilance",
                    "tarif": 6000,
                    "definition": "Élaboration d'un plan de vigilance conforme à la loi sur le devoir de vigilance des sociétés mères et donneuses d'ordre."
                },
                "conformite_concurrence": {
                    "label": "Programme de conformité concurrence",
                    "tarif": 4500,
                    "definition": "Élaboration d'un programme de conformité aux règles du droit de la concurrence."
                },

                # COMMERCE INTERNATIONAL
                "conseil_sanctions_internationales": {
                    "label": "Conseil en sanctions internationales",
                    "tarif": 5000,
                    "definition": "Assistance juridique sur la conformité aux régimes de sanctions internationales."
                },
                "conformite_exportation": {
                    "label": "Conformité contrôle des exportations",
                    "tarif": 4800,
                    "definition": "Conseil sur la conformité aux réglementations de contrôle des exportations."
                },

                # FORMATION ET DISPOSITIFS
                "formation_compliance": {
                    "label": "Formation compliance",
                    "tarif": 2500,
                    "definition": "Sessions de formation sur les enjeux de compliance pour les dirigeants et employés."
                },
                "dispositif_alerte": {
                    "label": "Mise en place de dispositif d'alerte",
                    "tarif": 3500,
                    "definition": "Création et implémentation d'un système d'alerte interne conforme aux exigences légales."
                },

                # ACCOMPAGNEMENT GLOBAL
                "externalisation_partielle": {
                    "label": "Externalisation juridique partielle",
                    "tarif": 2000,
                    "definition": "Accompagnement juridique sur des domaines spécifiques de l'entreprise, en complément des ressources internes existantes."
                }
            }
        },

        "externalisation_juridique": {
            "label": "Externalisation juridique",
            "prestations": {
                # EXTERNALISATION COMPLÈTE
                "externalisation_complete": {
                    "label": "Externalisation complète des fonctions juridiques",
                    "tarif": 2000,
                    "definition": "Accompagnement complet de l'entreprise dans toutes ses problématiques juridiques en lieu et place d'un service juridique interne."
                },

                # SOLUTIONS FLEXIBLES
                "externalisation_partielle": {
                    "label": "Externalisation juridique partielle",
                    "tarif": 1200,
                    "definition": "Accompagnement juridique sur des domaines spécifiques de l'entreprise, en complément des ressources internes existantes."
                },
                "conseil_juridique_ponctuel": {
                    "label": "Conseil juridique ponctuel",
                    "tarif": 800,
                    "definition": "Assistance juridique ponctuelle pour des besoins spécifiques de l'entreprise."
                },

                # AUDIT
                "audit_juridique_global": {
                    "label": "Audit juridique global",
                    "tarif": 3000,
                    "definition": "Évaluation complète de la situation juridique de l'entreprise et identification des besoins d'accompagnement."
                }
            }
        }
    }

def get_facteur_urgence():
    return 1.5  # Facteur multiplicateur pour les cas urgents
