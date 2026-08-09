# Decision log

This document represents a history of decisions made while developing this project. 
It is kept for tracking and learning purpose only.
---
| # | Date     | Decision                                                                                                                                                     |
|---|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| 0 | 08-08-26 | `/app/extensions.py`: Omit explicitelly calling DeclarativeBase in favor of using  Flask's db.Model that is effectively a declarative_base()-produced class. |
| 1 | 08-08-26 | `/app/___init___.py`: Omit explicetelly creating the SQLAlcemy engine. It happens inside`db.init_app()`.                                                     |
| 2 | 08-08-26 | `/app/blueprints/`: Decision to explore Flask's blueprints. May be redundant for an app of this size, but a valuable skill.