from exts import db

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))

    def __init__(self, name, email):
        self.name = name
        self.email = email

class ShortSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(users.id), primary_key=True, default=1)
    summary = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, summary, score):
        self.summary = summary
        self.score = score


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(users.id), primary_key=True)
    behaviouralAssessment = db.Column(db.Text)
    nonBehaviouralAssessment = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, behaviouralAssessment, nonBehaviouralAssessment, score):
        self.behaviouralAssessment = behaviouralAssessment
        self.nonBehaviouralAssessment = nonBehaviouralAssessment
        self.score = score


class PersonsConsulted(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    who = db.Column(db.Text)
    how = db.Column(db.Text)
    assessment_id = db.Column(db.Integer, db.ForeignKey(Assessment.id), nullable=False)

    def __init__(self, who, how, assessment_id):
        self.assessment_id = assessment_id
        self.how = how
        self.who = who


class BAFunction(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey(users.id), primary_key=True)
    functionName = db.Column(db.String(1000))
    description = db.Column(db.Text)
    summary = db.Column(db.Text)
    proposedAlternative = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, functionName, description, summary, proposedAlternative, score):
        self.functionName = functionName
        self.description = description
        self.summary = summary
        self.proposedAlternative = proposedAlternative
        self.score = score


class STC(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    settingEvents = db.Column(db.Text)
    trigger = db.Column(db.Text)
    consequences = db.Column(db.Text)
    f_id = db.Column(db.Integer, db.ForeignKey(BAFunction.id), nullable=False)

    def __init__(self, settingEvents, trigger, consequences, f_id):
        self.settingEvents = settingEvents
        self.trigger = trigger
        self.consequences = consequences
        self.f_id = f_id


class Goal(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey(users.id), primary_key=True)
    behaviour = db.Column(db.Text)
    life = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, behaviour, life, score):
        self.behaviour = behaviour
        self.life = life
        self.score = score


class Strategies(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey(users.id), primary_key=True)
    environment = db.Column(db.Text)
    teaching = db.Column(db.Text)
    others = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, environment, teaching, others, score):
        self.environment = environment
        self.teaching = teaching
        self.others = others
        self.score = score


class Reinforcement(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey(users.id), primary_key=True)
    reinforcer = db.Column(db.String(10000))
    schedule = db.Column(db.Text)
    howIdentified = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, reinforcer, schedule, howIdentified, score):
        self.reinforcer = reinforcer
        self.schedule = schedule
        self.howIdentified = howIdentified
        self.score = score


class DeEscalation(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey(users.id), primary_key=True)
    howtoPrompt = db.Column(db.Text)
    strategies = db.Column(db.Text)
    postIncident = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, howtoPrompt, strategies, postIncident, score):
        self.howtoPrompt = howtoPrompt
        self.strategies = strategies
        self.postIncident = postIncident
        self.score = score


class Intervention(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey(users.id), primary_key=True)
    type = db.Column(db.String(1000))
    ifProposed = db.Column(db.String(10))

    def __init__(self, type, ifProposed):
        self.type = type
        self.ifProposed = ifProposed


class ChemicalRestraint(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    iv_id = db.Column('iv_id', db.Integer, db.ForeignKey(Intervention.id), primary_key=True)
    positiveStrategy = db.Column(db.Text)
    circumstance = db.Column(db.Text)
    procedure = db.Column(db.Text)
    howRestrainReduce = db.Column(db.Text)
    why = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, positiveStrategy, circumstance, procedure, howRestrainReduce, why, score):
        self.positiveStrategy = positiveStrategy
        self.circumstance = circumstance
        self.procedure = procedure
        self.howRestrainReduce = howRestrainReduce
        self.why = why
        self.score = score


class Medication(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000))
    dosage = db.Column(db.String(1000))
    frequency = db.Column(db.String(1000))
    administration = db.Column(db.String(1000))
    route = db.Column(db.String(1000))
    prescriber = db.Column(db.String(1000))
    cr_id = db.Column(db.Integer, db.ForeignKey(ChemicalRestraint.id), nullable=False)

    def __init__(self, name, dosage, frequency, administration, route, prescriber, cr_id):
        self.name = name
        self.dosage = dosage
        self.frequency = frequency
        self.administration = administration
        self.route = route
        self.prescriber = prescriber
        self.cr_id = cr_id


class SocialValidity1(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    how = db.Column(db.Text)
    who = db.Column(db.Text)
    cr_id = db.Column(db.Integer, db.ForeignKey(ChemicalRestraint.id), nullable=False)

    def __init__(self, how, who, cr_id):
        self.how = how
        self.who = who
        self.cr_id = cr_id


class Authorisation1(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    authorisationBody = db.Column(db.String(1000))
    approvalPeriod = db.Column(db.String(1000))
    cr_id = db.Column(db.Integer, db.ForeignKey(ChemicalRestraint.id), nullable=False)

    def __init__(self, authorisationBody, approvalPeriod, cr_id):
        self.authorisationBody = authorisationBody
        self.approvalPeriod = approvalPeriod
        self.cr_id = cr_id


class PhysicalRestraint(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    iv_id = db.Column('iv_id', db.Integer, db.ForeignKey(Intervention.id), primary_key=True)
    description = db.Column(db.Text)
    positiveStrategy = db.Column(db.Text)
    circumstance = db.Column(db.Text)
    procedure = db.Column(db.Text)
    how = db.Column(db.Text)
    why = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, description, positiveStrategy, circumstance, procedure, how, why, score):
        self.description = description
        self.positiveStrategy = positiveStrategy
        self.circumstance = circumstance
        self.procedure = procedure
        self.how = how
        self.why = why
        self.score = score


class SocialValidity2(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    how = db.Column(db.Text)
    who = db.Column(db.Text)
    pr_id = db.Column(db.Integer, db.ForeignKey(PhysicalRestraint.id), nullable=False)

    def __init__(self, how, who, pr_id):
        self.how = how
        self.who = who
        self.pr_id = pr_id


class Authorisation2(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    authorisationBody = db.Column(db.String(1000))
    approvalPeriod = db.Column(db.String(1000))
    pr_id = db.Column(db.Integer, db.ForeignKey(PhysicalRestraint.id), nullable=False)

    def __init__(self, authorisationBody, approvalPeriod, pr_id):
        self.authorisationBody = authorisationBody
        self.approvalPeriod = approvalPeriod
        self.pr_id = pr_id


class MechanicalRestraint(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    iv_id = db.Column('iv_id', db.Integer, db.ForeignKey(Intervention.id), primary_key=True)
    description = db.Column(db.Text)
    frequency = db.Column(db.String(1000))
    positiveStrategy = db.Column(db.Text)
    circumstance = db.Column(db.Text)
    procedure = db.Column(db.Text)
    howKnow = db.Column(db.Text)
    howRestraint = db.Column(db.Text)
    why = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, description, positiveStrategy, circumstance, procedure, howKnow,howRestraint, why, frequency, score):
        self.frequency = frequency
        self.description = description
        self.positiveStrategy = positiveStrategy
        self.circumstance = circumstance
        self.procedure = procedure
        self.howKnow = howKnow
        self.howRestraint = howRestraint
        self.why = why
        self.score = score


class SocialValidity3(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    how = db.Column(db.Text)
    who = db.Column(db.Text)
    mr_id = db.Column(db.Integer, db.ForeignKey(MechanicalRestraint.id), nullable=False)

    def __init__(self, how, who, mr_id):
        self.how = how
        self.who = who
        self.mr_id = mr_id


class Authorisation3(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    authorisationBody = db.Column(db.String(1000))
    approvalPeriod = db.Column(db.String(1000))
    mr_id = db.Column(db.Integer, db.ForeignKey(MechanicalRestraint.id), nullable=False)

    def __init__(self, authorisationBody, approvalPeriod, mr_id):
        self.authorisationBody = authorisationBody
        self.approvalPeriod = approvalPeriod
        self.mr_id = mr_id


class EnvironmentalRestraint(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    iv_id = db.Column('iv_id', db.Integer, db.ForeignKey(Intervention.id), primary_key=True)
    description = db.Column(db.Text)
    frequency = db.Column(db.String(1000))
    positiveStrategy = db.Column(db.Text)
    circumstance = db.Column(db.Text)
    person = db.Column(db.Text)
    procedure = db.Column(db.Text)
    impact = db.Column(db.String(1000))
    howImpact = db.Column(db.Text)
    howRestraint = db.Column(db.Text)
    why = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, description, positiveStrategy, circumstance, procedure, howImpact, howRestraint, impact, why
                 , frequency, person, score):
        self.frequency = frequency
        self.description = description
        self.positiveStrategy = positiveStrategy
        self.circumstance = circumstance
        self.procedure = procedure
        self.howImpact = howImpact
        self.howRestraint = howRestraint
        self.impact = impact
        self.person = person
        self.why = why
        self.score = score


class SocialValidity4(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    how = db.Column(db.Text)
    who = db.Column(db.Text)
    er_id = db.Column(db.Integer, db.ForeignKey(EnvironmentalRestraint.id), nullable=False)

    def __init__(self, how, who, er_id):
        self.how = how
        self.who = who
        self.er_id = er_id


class Authorisation4(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    authorisationBody = db.Column(db.String(1000))
    approvalPeriod = db.Column(db.String(1000))
    er_id = db.Column(db.Integer, db.ForeignKey(EnvironmentalRestraint.id), nullable=False)

    def __init__(self, authorisationBody, approvalPeriod, er_id):
        self.authorisationBody = authorisationBody
        self.approvalPeriod = approvalPeriod
        self.er_id = er_id


class SeclusionRestraint(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    iv_id = db.Column('iv_id', db.Integer, db.ForeignKey(Intervention.id), primary_key=True)
    frequency = db.Column(db.String(1000))
    positiveStrategy = db.Column(db.Text)
    circumstance = db.Column(db.Text)
    maxFrequency = db.Column(db.Text)
    procedure = db.Column(db.Text)
    how = db.Column(db.Text)
    why = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, frequency, positiveStrategy, circumstance, maxFrequency, procedure, how, why, score):
        self.frequency = frequency
        self.maxFrequency = maxFrequency
        self.positiveStrategy = positiveStrategy
        self.circumstance = circumstance
        self.procedure = procedure
        self.how = how
        self.why = why
        self.score = score


class SocialValidity5(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    how = db.Column(db.Text)
    who = db.Column(db.Text)
    sr_id = db.Column(db.Integer, db.ForeignKey(SeclusionRestraint.id), nullable=False)

    def __init__(self, how, who, sr_id):
        self.how = how
        self.who = who
        self.sr_id = sr_id


class Authorisation5(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    authorisationBody = db.Column(db.String(1000))
    approvalPeriod = db.Column(db.String(1000))
    sr_id = db.Column(db.Integer, db.ForeignKey(SeclusionRestraint.id), nullable=False)

    def __init__(self, authorisationBody, approvalPeriod, sr_id):
        self.authorisationBody = authorisationBody
        self.approvalPeriod = approvalPeriod
        self.sr_id = sr_id


class Implementation(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey(users.id), primary_key=True)
    people = db.Column(db.String(1000))
    timeframe = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, people, timeframe, score):
        self.people = people
        self.timeframe = timeframe
        self.score = score


class HowImplementer(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    strategy = db.Column(db.Text)
    responsible = db.Column(db.Text)
    i_id = db.Column(db.Integer, db.ForeignKey(Implementation.id), nullable=False)

    def __init__(self, strategy, responsible, i_id):
        self.strategy = strategy
        self.responsible = responsible
        self.i_id = i_id


class HowCommunicate(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    strategy = db.Column(db.Text)
    responsible = db.Column(db.Text)
    i_id = db.Column(db.Integer, db.ForeignKey(Implementation.id), nullable=False)

    def __init__(self, strategy, responsible, i_id):
        self.strategy = strategy
        self.responsible = responsible
        self.i_id = i_id


class HowImplementation(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    strategy = db.Column(db.Text)
    responsible = db.Column(db.Text)
    i_id = db.Column(db.Integer, db.ForeignKey(Implementation.id), nullable=False)

    def __init__(self, strategy, responsible, i_id):
        self.strategy = strategy
        self.responsible = responsible
        self.i_id = i_id


class ImplementationPlan(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.Text)
    responsible = db.Column(db.Text)
    ip_id = db.Column(db.Integer, db.ForeignKey(Implementation.id), nullable=False)

    def __init__(self, action, responsible, ip_id):
        self.action = action
        self.responsible = responsible
        self.ip_id = ip_id


class SocialV(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey(users.id), primary_key=True)
    acceptability = db.Column(db.Text)
    who = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, acceptability, who, score):
        self.acceptability = acceptability
        self.who = who
        self.score = score
