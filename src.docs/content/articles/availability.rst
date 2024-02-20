Availability calculation in "nines" notation
############################################

:summary: Estimating one of SRE's most common SLO
:date: 2024-02-18 20:50:49
:category: article
:tags: sre
:slug: availability

The rapidly growing interest in clouds, distributed systems, microservice architecture, and service-oriented applications has led to the emergence of a new branch of computer systems engineering - *Site Reliability Engineering* (SRE). One of the primary goals of the SRE is to ensure that a service meets certain requirements for production readiness. Services are generally considered to be *production* when they can be trusted and relied upon. A service provider and the customers, who usually pay for a service, document a common understanding of trust in a *Service Level Agreement* (SLA). It contains all expectations in the form of *Service Level Objectives* (SLO) and penalties if these expectations are not met. SLOs are **performance** and **availability** goals for a production service, defined on an annual time scale. These are the system characteristics that are both the most valuable to customers and worth committing to keep them within the defined expectations. SLOs are carefully quantified using *Service Level Indicators* (SLI). SLIs are chosen specifically for SLOs as a measurable form of some properties. It can be a metric or a value derived from logs. SLIs are typically sampled over a much shorter periods of time, from tens of seconds to a few minutes, and then a mean or an average distribution is applied to obtain a value.

|

*Site Reliability Engineers*, in turn, are responsible for ensuring that production services meet all target SLOs defined in the SLA. They do this by focusing on the reliability through a set of practices that are more or less standardized across the industry. Some of the most common practices include:

* Continuous monitoring of availability and performance characteristics;
* Troubleshooting failures and eliminating degradation issues;
* Improving overall stability and scalability through automation to keep all key metrics within expected ranges;
* Preparing for disaster recovery through continuous stress testing using the error budget, an agreed upon timeframe in which a service can be degraded or unavailable.

|

Performance SLOs are important goals, but they are only important if a service is available. Availability is so important that it's sometimes *mistakenly* considered the only SLA component. Finding the right SLI to measure availability can be challenging. It's service-specific and depends on a variety of factors, such as the underlying infrastructure, architecture, etc. In SLO form, availability is expressed as a percentage in what is called "nines" notation. For example, in the clouds, the most common availability SLO is 99.9%, which is called "3-nines". However, you are unlikely to find it higher than 99.999%, or "5-nines". This percentage is basically a ratio of the time a service is available to the total uptime (which includes downtime), calculated over the past year.

|

It is interesting that people who use the nines notation are actually referring to the time when a service is a sort of allowed to be down. This downtime, which is literally allowed by the SLA, forms what is  called the *error budget*. While targeting 100% availability is hardly feasible, it turns out that from a practical point of view, it is more beneficial to commit to a lower availability. Even if all technical possibilities exist to provide more "nines".  At certain levels, services with a higher availability will not be noticed by the majority of customers, so it's probably not worth the effort. However, having some error budget opens the doors to experimentation and less stressful deployments of new product features.

|

It is useful to know how to actually calculate the amount of time when your system is allowed to be out of service. To do this, remember that the availability SLO is defined for a one-year period. So,  *60s by 60m by 24h by 365d* gives us *31536000* seconds of a total uptime. Then, if the availability is "five-nines" (99.999%), then the downtime is 0.001%, or `31536000 * 0.00001 = 315.36` sec, which is about *5.256* minutes per year that the service can be down. A similar calculation for "three-nines" (99.9%) availability shows that the service can be down for `31536000 * 0.001 = 31536` seconds, or 525.6 minutes, or *8.76* hours per year.

|

Summary
-------

* Site Reliability Engineering (SRE) focuses on ensuring production services meet requirements for production readiness and can be trusted and relied upon.
* A Service Level Agreement (SLA) contains expectations in the form of Service Level Objectives (SLOs) and penalties if not met.
* SLOs define annual performance and availability goals for production services.
* Service Level Indicators (SLIs) are metrics chosen to measure SLOs, sampled over short periods like seconds to minutes.
* SREs ensure services meet SLOs through standardized practices like monitoring, emergency response, and capacity planning.
* Availability is the most important SLA component and is expressed as percentages or "nines" denoting hours of annual downtime allowed.
* The 99.9% availability SLO allows 8.76 hours of annual downtime while 99.999% allows 5.256 minutes.
* Allowing some downtime forms an "error budget" even if 100% uptime is technically possible.
* Higher availability beyond a certain level may not be noticeable to most customers.
* Calculating allowed downtime involves determining the total seconds in a year and applying the percentage downtime allowed.

|

