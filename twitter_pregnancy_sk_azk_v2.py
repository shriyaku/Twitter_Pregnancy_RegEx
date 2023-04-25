import pandas as pd
import re
from datetime import *
from dateutil.relativedelta import *

regex_digits = re.compile(r"\d+")

def preprocess(tweet):
    tweet = re.sub(r"one", "1", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"two", "2", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"three", "3", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"four", "4", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"five", "5", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"six", "6", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"seven", "7", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"eight", "8", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"nine", "9", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"ten", "10", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"\ba\W+(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\b", "1 month", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"\ba\W+(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\b", "1 week", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"\ba\W*few\b", "3", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"\ba\W*couple(\W*of)?\b", "2", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"(\d+)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\s*/\s*(\d+)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)", r"\3 \4", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"(\d+)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\s*/\s*(\d+)\W*(dayd|dyas|days)", r"\3 \4", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"(\d+)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\s*/\s*(\d+)\W*(dayd|dyas|days)", r"\3 \4", tweet, flags=re.IGNORECASE)

    return tweet


def extract_pregnancy_timeframe(tweet, date):
    # [1] i'm X months pregnant
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([a-z]+\W*)?([1-9]|10|one|two|three|four|five|six|seven|eight|nine|ten)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\W*(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregy|preggy)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        delta = relativedelta(months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [2] i'm X months in to my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([a-z]+\W*)?([1-9]|10|one|two|three|four|five|six|seven|eight|nine|ten)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\W*(in\W*to|along\W*in)\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        delta = relativedelta(months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [3] i'm X weeks pregnant
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([a-z]+\W*)?([5-9]|[1-3][0-9]|4[0-2]|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregy|preggy)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        delta = relativedelta(weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [4] i'm X weeks in to my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([a-z]+\W*)?([5-9]|[1-3][0-9]|4[0-2]|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(in\W*to|along\W*in)\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        delta = relativedelta(weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [5] i'm X days pregnant
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([a-z]+\W*)?([3-9][0-9]|[1-2][0-9][0-9])\W*(dayd|dyas|days)\W*(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregy|preggy)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_days = int(match_digits[0])
        delta = relativedelta(days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [6] i'm X days in to my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([a-z]+\W*)?([3-9][0-9]|[1-2][0-9][0-9])\W*(dayd|dyas|days)\W*(in\W*to|along\W*in)\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_days = int(match_digits[0])
        delta = relativedelta(days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [7] i'm X months and Y weeks pregnant
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([1-9]|10|one|two|three|four|five|six|seven|eight|nine|ten)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-3][0-9]|4[0-2]|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregy|preggy)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        delta = relativedelta(weeks=quantity_weeks, months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [8] i'm X months and Y weeks in to my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([1-9]|10|one|two|three|four|five|six|seven|eight|nine|ten)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-3][0-9]|4[0-2]|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(in\W*to|along\W*in)\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        delta = relativedelta(weeks=quantity_weeks, months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date+ relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [9] i'm X months and Y days pregnant
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([a-z]+\W*)?([1-9]|10|one|two|three|four|five|six|seven|eight|nine|ten)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-9][0-9]|[1-2][0-9][0-9]|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(dayd|dyas|days|day)\W*(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregy|preggy)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(days=quantity_days, months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [10] i'm months and days in to my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([a-z]+\W*)?([1-9]|10|one|two|three|four|five|six|seven|eight|nine|ten)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-9][0-9]|[1-2][0-9][0-9]|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(dayd|dyas|days|day)\W*(in\W*to|along\W*in)\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(days=quantity_days, months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [11] i'm X months, Y weeks, and Z days pregnant
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([a-z]+\W*)?([1-9]|10|one|two|three|four|five|six|seven|eight|nine|ten)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-3][0-9]|4[0-2]|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|[1-2][0-9][0-9]|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(dayd|dyas|days|day)\W*(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregy|preggy)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        quantity_days = int(match_digits[2])
        delta = relativedelta(days=quantity_days, weeks=quantity_weeks, months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [12] i'm X months, Y weeks, and Z days in to my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([a-z]+\W*)?([1-9]|10|one|two|three|four|five|six|seven|eight|nine|ten)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-3][0-9]|4[0-2]|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|[1-2][0-9][0-9]|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(dayd|dyas|days|day)\W*(in\W*to|along\W*in)\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        quantity_days = int(match_digits[2])
        delta = relativedelta(days=quantity_days, weeks=quantity_weeks, months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [13] i'm X weeks and Y days pregnant
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([a-z]+\W*)?([5-9]|[1-3][0-9]|4[0-2]|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|[1-2][0-9][0-9]|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(dayd|dyas|days|day)\W*(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregy|preggy)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(days=quantity_days, weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [14] i'm X weeks and Y days in to my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([a-z]+\W*)?([5-9]|[1-3][0-9]|4[0-2]|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|[1-2][0-9][0-9]|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(dayd|dyas|days|day)\W*(in\W*to|along\W*in)\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(days=quantity_days, weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [15] #Xmonthspregnant
    if match := re.search(r'#([1-9]|10|one|two|three|four|five|six|seven|eight|nine|ten)(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregy|preggy)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        delta = relativedelta(months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [16] #Xweekspregnant
    if match := re.search(r'#([5-9]|[1-3][0-9]|4[0-2]|five|six|seven|eight|nine|ten)(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregy|preggy)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        delta = relativedelta(weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [17] #Xmonths...pregnancy
    if match := re.search(r'#([1-9]|10|one|two|three|four|five|six|seven|eight|nine|ten)(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\b.+\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        delta = relativedelta(months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [18] pregnancy...#Xmonths
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|belly)\b.+#([1-9]|10|one|two|three|four|five|six|seven|eight|nine|ten)(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'#([1-9]|10|one|two|three|four|five|six|seven|eight|nine|ten)(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_months = int(match_digits[0])
            delta = relativedelta(months=quantity_months)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_start_date = date - delta
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [19] #Xweeks...pregnancy
    if match := re.search(r'#([5-9]|[1-3][0-9]|4[0-2]|five|six|seven|eight|nine|ten)(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\b.+\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        delta = relativedelta(weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_start_date = date - delta
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [20] pregnancy...#Xweeks
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.+#([5-9]|[1-3][0-9]|4[0-2]|five|six|seven|eight|nine|ten)(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\b', tweet, flags=re.IGNORECASE):

        if match:= re.search(r'#([5-9]|[1-3][0-9]|4[0-2]|five|six|seven|eight|nine|ten)(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_weeks = int(match_digits[0])
            delta = relativedelta(weeks=quantity_weeks)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_start_date = date - delta
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [21] X months until my due date
    if match := re.search(r'(?<!was\W)\b([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\W*((untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)|(awae|awy|awat|aways|away|wawy|awey|awway|awya)\W*(frome|frrom|from|frum|fron|frmo|fromo|fromn|fro|froom|fromt|frm|drom|fom|froma|ftom|ffrom))\W*my\W*due\W*date\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        delta = relativedelta(months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [22] X months until my baby is due
    if match := re.search(r'\b([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*my\W*baby\W*((boy|girl)\W*)?(is|s)\W*due\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        delta = relativedelta(months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [23] X months until i'm due...baby
    if match := re.search(r'\b([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        delta = relativedelta(months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [24] baby...X months until i'm due
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*\b([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'\b([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_months = int(match_digits[0])
            delta = relativedelta(months=quantity_months)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [25a] X months and Y weeks until my due date
    if match := re.search(r'(?<!was\W)\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*((untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)|(awae|awy|awat|aways|away|wawy|awey|awway|awya)\W*(frome|frrom|from|frum|fron|frmo|fromo|fromn|fro|froom|fromt|frm|drom|fom|froma|ftom|ffrom))\W*my\W*due\W*date\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        delta = relativedelta(months=quantity_months, weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [25b] X weeks until my due date
    if match := re.search(r'(?<!was\W)\b([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*((untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)|(awae|awy|awat|aways|away|wawy|awey|awway|awya)\W*(frome|frrom|from|frum|fron|frmo|fromo|fromn|fro|froom|fromt|frm|drom|fom|froma|ftom|ffrom))\W*my\W*due\W*date\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        delta = relativedelta(weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [26a] X months and Y weeks until my baby is due
    if match := re.search(r'\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*my\W*baby\W*((boy|girl)\W*)?(is|s)\W*due\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        delta = relativedelta(months=quantity_months, weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [26b] X weeks until my baby is due
    if match := re.search(r'\b([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*my\W*baby\W*((boy|girl)\W*)?(is|s)\W*due\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        delta = relativedelta(weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [27a] X months and Y weeks until i'm due...baby
    if match := re.search(r'\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        delta = relativedelta(months=quantity_months, weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [27b] X weeks until i'm due...baby
    if match := re.search(r'\b([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        delta = relativedelta(weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [28a] baby...X months and Y weeks until i'm due
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a(?!m)|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_months = int(match_digits[0])
            quantity_weeks = int(match_digits[1])
            delta = relativedelta(months=quantity_months, weeks=quantity_weeks)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [28b] baby...X weeks until i'm due
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*\b([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'\b([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_weeks = int(match_digits[0])
            delta = relativedelta(weeks=quantity_weeks)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [29a] X months, Y weeks, and Z days until my due date
    if match := re.search(r'(?<!was\W)\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*((untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)|(awae|awy|awat|aways|away|wawy|awey|awway|awya)\W*(frome|frrom|from|frum|fron|frmo|fromo|fromn|fro|froom|fromt|frm|drom|fom|froma|ftom|ffrom))\W*my\W*due\W*date\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        quantity_days = int(match_digits[2])
        delta = relativedelta(months=quantity_months,weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [29b] X months and Y days until my due date
    if match := re.search(r'(?<!was\W)\b([1-5]|a(?!m\b)|one|two|three|four|five|couple|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*((untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)|(awae|awy|awat|aways|away|wawy|awey|awway|awya)\W*(frome|frrom|from|frum|fron|frmo|fromo|fromn|fro|froom|fromt|frm|drom|fom|froma|ftom|ffrom))\W*my\W*due\W*date\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(months=quantity_months, days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [29c] X weeks and Y days until my due date
    if match := re.search(r'(?<!was\W)\b([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*((untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)|(awae|awy|awat|aways|away|wawy|awey|awway|awya)\W*(frome|frrom|from|frum|fron|frmo|fromo|fromn|fro|froom|fromt|frm|drom|fom|froma|ftom|ffrom))\W*my\W*due\W*date\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(weeks=quantity_weeks, days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [29d] X days until my due date
    if match := re.search(r'(?<!was\W)\b([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*((untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)|(awae|awy|awat|aways|away|wawy|awey|awway|awya)\W*(frome|frrom|from|frum|fron|frmo|fromo|fromn|fro|froom|fromt|frm|drom|fom|froma|ftom|ffrom))\W*my\W*due\W*date\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_days = int(match_digits[0])
        delta = relativedelta(days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [30a] X months, Y weeks, and Z days until my baby is due
    if match := re.search(r'\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*my\W*baby\W*((boy|girl)\W*)?(is|s)\W*due\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        quantity_days = int(match_digits[2])
        delta = relativedelta(months=quantity_months,weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [30b] X months and Y days until my baby is due
    if match := re.search(r'\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*my\W*baby\W*((boy|girl)\W*)?(is|s)\W*due\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(months=quantity_months,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [30c] X weeks and Y days until my baby is due
    if match := re.search(r'\b([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*my\W*baby\W*((boy|girl)\W*)?(is|s)\W*due\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [30d] X days until my baby is due
    if match := re.search(r'\b([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*my\W*baby\W*((boy|girl)\W*)?(is|s)\W*due\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_days = int(match_digits[0])
        delta = relativedelta(days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [31a] X months, Y weeks, and Z days until i'm due...baby
    if match := re.search(r'\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        quantity_days = int(match_digits[2])
        delta = relativedelta(months=quantity_months,weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [31b] X months and Y days until i'm due...baby
    if match := re.search(r'\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(months=quantity_months,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [31c] X weeks and Y days until i'm due...baby
    if match := re.search(r'\b([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [31d] X days until i'm due...baby
    if match := re.search(r'\b([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_days = int(match_digits[0])
        delta = relativedelta(days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [32a] baby...X months, Y weeks, and Z days until i'm due
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_months = int(match_digits[0])
            quantity_weeks = int(match_digits[1])
            quantity_days = int(match_digits[2])
            delta = relativedelta(months=quantity_months,weeks=quantity_weeks,days=quantity_days)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [32b] baby...X months and Y days until i'm due
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'\b([1-5]|a(?!m\b)|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_months = int(match_digits[0])
            quantity_days = int(match_digits[1])
            delta = relativedelta(months=quantity_months,days=quantity_days)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [32c] baby...X weeks and Y days until i'm due
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*\b([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'\b([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_weeks = int(match_digits[0])
            quantity_days = int(match_digits[1])
            delta = relativedelta(weeks=quantity_weeks,days=quantity_days)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [32d] baby...X days until i'm due
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*\b([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'\b([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(untill|unil|untili|till|ubtil|unitl|untll|until|til|intil|unttil|intill|unti|unill|untl|untiil|ntil|untii)\W*i(\s*am|\W*m)\W*due\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_days = int(match_digits[0])
            delta = relativedelta(days=quantity_days)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [33a] my due date is in X months, Y weeks, and Z days
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        quantity_days = int(match_digits[2])
        delta = relativedelta(months=quantity_months,weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [33b] my due date is in months and weeks
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(months=quantity_months,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [33c] my due date is in X months and Y days
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(months=quantity_months,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [33d] my due date is in X months
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        delta = relativedelta(months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [34a] i'm due in X months, Y weeks, and Z days...baby
    if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        quantity_days = int(match_digits[2])
        delta = relativedelta(months=quantity_months,weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [34b] i'm due in X months and Y weeks...baby
    if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        delta = relativedelta(months=quantity_months,weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [34c] i'm due in X months and Y days...baby
    if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [34d] i'm due in X months...baby
    if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        delta = relativedelta(months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [35a] baby...i'm due in X months, Y weeks, and Z days
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_months = int(match_digits[0])
            quantity_weeks = int(match_digits[1])
            quantity_days = int(match_digits[2])
            delta = relativedelta(months=quantity_months,weeks=quantity_weeks,days=quantity_days)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [35b] baby...i'm due in X months and Y weeks
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_months = int(match_digits[0])
            quantity_weeks = int(match_digits[1])
            delta = relativedelta(months=quantity_months,weeks=quantity_weeks)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [35c] baby...i'm due in X months and Y days
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_months = int(match_digits[0])
            quantity_days = int(match_digits[1])
            delta = relativedelta(months=quantity_months,days=quantity_days)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [35d] baby...X days until i'm due
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_days = int(match_digits[0])
            delta = relativedelta(days=quantity_days)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [36a] my due date is in X weeks and Y days
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*in\W*(([a-z]+|less\W*than)\W*)?([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [36b] my due date is in X weeks
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*in\W*(([a-z]+|less\W*than)\W*)?([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        delta = relativedelta(weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [37a] my due date is in X weeks and Y days
    if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [37b] i'm due in X weeks...baby
    if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        delta = relativedelta(weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [38a] baby...i'm due in X weeks and Y days
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)(and|\W|amp)*([1-9]|[1-9][0-9]|100|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_weeks = int(match_digits[0])
            quantity_days = int(match_digits[1])
            delta = relativedelta(weeks=quantity_weeks,days=quantity_days)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [38b] baby...i'm due in X weeks
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_weeks = int(match_digits[0])
            delta = relativedelta(weeks=quantity_weeks)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [39] my due date is in X days
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*in\W*([a-z]+\W*)?([1-9]|[1-9][0-9]|100|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_days = int(match_digits[0])
        delta = relativedelta(days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [40] i'm due in X days...baby
    if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-9]|[1-9][0-9]|100|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_days = int(match_digits[0])
        delta = relativedelta(days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [41] baby...i'm due in X days
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-9]|[1-9][0-9]|100|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*in\W*(([a-z]+|less\W*than)\W*)?([1-9]|[1-9][0-9]|100|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            quantity_days = int(match_digits[0])
            delta = relativedelta(days=quantity_days)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pregnancy_end_date = date + delta
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [42] my due date is X months away
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*(?!not)(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\W*(awae|awy|awat|aways|away|wawy|awey|awway|awya)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        delta = relativedelta(months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [43] my due date is X weeks away
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*(?!not)(([a-z]+|less\W*than)\W*)?([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(awae|awy|awat|aways|away|wawy|awey|awway|awya)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        delta = relativedelta(weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [44] my due date is X days away
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*(?!not)([a-z]+\W*)?([1-9]|[1-9][0-9]|100|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(awae|awy|awat|aways|away|wawy|awey|awway|awya)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_days = int(match_digits[0])
        delta = relativedelta(days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [45] my due date is X months and Y weeks away
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*(?!not)([a-z]+\W*)?([1-5]|a|one|two|three|four|five)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(awae|awy|awat|aways|away|wawy|awey|awway|awya)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        delta = relativedelta(months=quantity_months,weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [46] my due date is X months and Y days away
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*(?!not)([a-z]+\W*)?([1-5]|a|one|two|three|four|five)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-9][0-9]|100|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(dayd|dyas|days|day)\W*(awae|awy|awat|aways|away|wawy|awey|awway|awya)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(months=quantity_months,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [47] my due date is X months, Y weeks, and Z days away
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*(?!not)([a-z]+\W*)?([1-5]|a|one|two|three|four|five)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(and|\W|amp)*([1-9]|[1-9][0-9]|100|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(dayd|dyas|days|day)\W*(awae|awy|awat|aways|away|wawy|awey|awway|awya)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        quantity_days = int(match_digits[2])
        delta = relativedelta(months=quantity_months,weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [48] my due date is X weeks and Y days away
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*(?!not)([a-z]+\W*)?([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(and|\W|amp)*([1-9]|[1-9][0-9]|100|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(dayd|dyas|days|day)\W*(awae|awy|awat|aways|away|wawy|awey|awway|awya)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [49] my due date is tomorrow
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*(tommor|tomorrows|tomoroww|tomorwo|tomororw|tomorroe|omorrow|2morrows|tomorror|tomorrow|tommow|tomro|tommarrow|tomoorow|2morrow|tommrrow|tmorrow|tomorrrow|tommarow|2morro|tomrw|2morow|tomorow|tomrorrow|tomoorw|tmrrw|toorrow|tomoorrow|tommorro|tommorow|tommorrows|tomarow|tommorrow|tommrow|tomrorow|tommorows|tomrow|tomarro|tmrw|tommorw|tomrrow|tomoro|tomorrw|tomor|tomorw|tomorro|tomarrow|tormorrow|tommoro)\b', tweet, flags=re.IGNORECASE):

        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + relativedelta(days=1)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [50] tomorrow is my due date
    if match := re.search(r'(?<!like\W)(?<!if\W)\b(tommor|tomorrows|tomoroww|tomorwo|tomororw|tomorroe|omorrow|2morrows|tomorror|tomorrow|tommow|tomro|tommarrow|tomoorow|2morrow|tommrrow|tmorrow|tomorrrow|tommarow|2morro|tomrw|2morow|tomorow|tomrorrow|tomoorw|tmrrw|toorrow|tomoorrow|tommorro|tommorow|tommorrows|tomarow|tommorrow|tommrow|tomrorow|tommorows|tomrow|tomarro|tmrw|tommorw|tomrrow|tomoro|tomorrw|tomor|tomorw|tomorro|tomarrow|tormorrow|tommoro)\W*(is|s)\W*my\W*due\W*date\b', tweet, flags=re.IGNORECASE):

        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + relativedelta(days=1)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [51] my due date is today
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*(tofday|tday|tody|todya|todat|toay|2day|today)\b', tweet, flags=re.IGNORECASE):

        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [52] today is my due date
    if match := re.search(r'(?<!like\W)(?<!if\W)\b(tofday|tday|tody|todya|todat|toay|2day|today)\W*(is|s)\W*my\W*due\W*date\b', tweet, flags=re.IGNORECASE):

        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [53] my due date was yesterday
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*was\W*(yeaterday|ysterday|yestersay|yestarday|yetserday|yesteray|ystrdy|yestrday|yestaday|yestersday|yesterady|yessterday|yestorday|yesturday|yeserday|yesterdat|yeasterday|yesterday|yeturday|yersterday|yesteday|yeterday|yesterdy|yestereday)\b', tweet, flags=re.IGNORECASE):

        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date - relativedelta(days=1)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [54] yesterday was my due date
    if match := re.search(r'(?<!like\W)(?<!if\W)\b(yeaterday|ysterday|yestersay|yestarday|yetserday|yesteray|ystrdy|yestrday|yestaday|yestersday|yesterady|yessterday|yestorday|yesturday|yeserday|yesterdat|yeasterday|yesterday|yeturday|yersterday|yesteday|yeterday|yesterdy|yestereday)\W*was\W*my\W*due\W*date\b', tweet, flags=re.IGNORECASE):

        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date - relativedelta(days=1)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [55] my due date is [day of the week]
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*((on|this)\W*)?(monday|monhay|moday|mondat|onday|mondays|mon|tuesday|tuedsday|tuesay|tuseday|tusday|teusday|tiesday|tues|tueday|wednesday|wenesday|wednsday|wedneday|wedsnesday|weekday|wendesday|wednesay|wdnesday|wensday|wedensday|wendsday|wednessday|wednes|wed|thursday|thusday|thursdsay|thrusday|thurdsday|thrursday|thurday|thurs|thursda|thursaday|thurdsay|thrurday|tursday|thuresday|thirsday|thursay|thursady|friday|froday|fri|saturday|satuday|saturady|saterday|saturaday|saturdy|staurday|satuarday|sturday|satuerday|saurday|sat|sunday|sun)\b', tweet, flags=re.IGNORECASE):

        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        if re.search(r'(monday|monhay|moday|mondat|onday|mondays|mon)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=MO)
        elif re.search(r'(tuesday|tuedsday|tuesay|tuseday|tusday|teusday|tiesday|tues|tueday)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=TU)
        elif re.search(r'(wednesday|wenesday|wednsday|wedneday|wedsnesday|weekday|wendesday|wednesay|wdnesday|wensday|wedensday|wendsday|wednessday|wednes|wed)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=WE)
        elif re.search(r'(thursday|thusday|thursdsay|thrusday|thurdsday|thrursday|thurday|thurs|thursda|thursaday|thurdsay|thrurday|tursday|thuresday|thirsday|thursay|thursady)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=TH)
        elif re.search(r'(friday|froday|fri)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=FR)
        elif re.search(r'(saturday|satuday|saturady|saterday|saturaday|saturdy|staurday|satuarday|sturday|satuerday|saurday|sat)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=SA)
        elif re.search(r'(sunday|sun)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=SU)

        if pregnancy_end_date == date:
            pregnancy_end_date = pregnancy_end_date + relativedelta(days=7)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")

        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [56] i'm due [day of the week]...baby
    if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(monday|monhay|moday|mondat|onday|mondays|mon|tuesday|tuedsday|tuesay|tuseday|tusday|teusday|tiesday|tues|tueday|wednesday|wenesday|wednsday|wedneday|wedsnesday|weekday|wendesday|wednesay|wdnesday|wensday|wedensday|wendsday|wednessday|wednes|wed|thursday|thusday|thursdsay|thrusday|thurdsday|thrursday|thurday|thurs|thursda|thursaday|thurdsay|thrurday|tursday|thuresday|thirsday|thursay|thursady|friday|froday|fri|saturday|satuday|saturady|saterday|saturaday|saturdy|staurday|satuarday|sturday|satuerday|saurday|sat|sunday|sun)\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        if re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(monday|monhay|moday|mondat|onday|mondays|mon)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=MO)
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(tuesday|tuedsday|tuesay|tuseday|tusday|teusday|tiesday|tues|tueday)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=TU)
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(wednesday|wenesday|wednsday|wedneday|wedsnesday|weekday|wendesday|wednesay|wdnesday|wensday|wedensday|wendsday|wednessday|wednes|wed)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=WE)
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(thursday|thusday|thursdsay|thrusday|thurdsday|thrursday|thurday|thurs|thursda|thursaday|thurdsay|thrurday|tursday|thuresday|thirsday|thursay|thursady)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=TH)
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(friday|froday|fri)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=FR)
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(saturday|satuday|saturady|saterday|saturaday|saturdy|staurday|satuarday|sturday|satuerday|saurday|sat)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=SA)
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(sunday|sun)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=SU)

        if pregnancy_end_date == date:
            pregnancy_end_date = pregnancy_end_date + relativedelta(days=7)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [57] baby...i'm due [day of the week]
    if match := re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(monday|monhay|moday|mondat|onday|mondays|mon|tuesday|tuedsday|tuesay|tuseday|tusday|teusday|tiesday|tues|tueday|wednesday|wenesday|wednsday|wedneday|wedsnesday|weekday|wendesday|wednesay|wdnesday|wensday|wedensday|wendsday|wednessday|wednes|wed|thursday|thusday|thursdsay|thrusday|thurdsday|thrursday|thurday|thurs|thursda|thursaday|thurdsay|thrurday|tursday|thuresday|thirsday|thursay|thursady|friday|froday|fri|saturday|satuday|saturady|saterday|saturaday|saturdy|staurday|satuarday|sturday|satuerday|saurday|sat|sunday|sun)\b', tweet, flags=re.IGNORECASE):

        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        if re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(monday|monhay|moday|mondat|onday|mondays|mon)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=MO)
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(tuesday|tuedsday|tuesay|tuseday|tusday|teusday|tiesday|tues|tueday)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=TU)
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(wednesday|wenesday|wednsday|wedneday|wedsnesday|weekday|wendesday|wednesay|wdnesday|wensday|wedensday|wendsday|wednessday|wednes|wed)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=WE)
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(thursday|thusday|thursdsay|thrusday|thurdsday|thrursday|thurday|thurs|thursda|thursaday|thurdsay|thrurday|tursday|thuresday|thirsday|thursay|thursady)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=TH)
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(friday|froday|fri)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=FR)
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(saturday|satuday|saturady|saterday|saturaday|saturdy|staurday|satuarday|sturday|satuerday|saurday|sat)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=SA)
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*((on|this)\W*)?(sunday|sun)\b', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=SU)

        if pregnancy_end_date == date:
            pregnancy_end_date = pregnancy_end_date + relativedelta(days=7)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [58] [day of the week] is my due date
    if match := re.search(r'(?<!like\W)(?<!if\W)\b(monday|monhay|moday|mondat|onday|mondays|mon|tuesday|tuedsday|tuesay|tuseday|tusday|teusday|tiesday|tues|tueday|wednesday|wenesday|wednsday|wedneday|wedsnesday|weekday|wendesday|wednesay|wdnesday|wensday|wedensday|wendsday|wednessday|wednes|wed|thursday|thusday|thursdsay|thrusday|thurdsday|thrursday|thurday|thurs|thursda|thursaday|thurdsay|thrurday|tursday|thuresday|thirsday|thursay|thursady|friday|froday|fri|saturday|satuday|saturady|saterday|saturaday|saturdy|staurday|satuarday|sturday|satuerday|saurday|sat|sunday|sun)\W*(is|s)\W*my\W*due\W*date\b', tweet, flags=re.IGNORECASE):

        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        if re.search(r'(monday|monhay|moday|mondat|onday|mondays|mon)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=MO)
        elif re.search(r'(tuesday|tuedsday|tuesay|tuseday|tusday|teusday|tiesday|tues|tueday)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=TU)
        elif re.search(r'(wednesday|wenesday|wednsday|wedneday|wedsnesday|weekday|wendesday|wednesay|wdnesday|wensday|wedensday|wendsday|wednessday|wednes|wed)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=WE)
        elif re.search(r'(thursday|thusday|thursdsay|thrusday|thurdsday|thrursday|thurday|thurs|thursda|thursaday|thurdsay|thrurday|tursday|thuresday|thirsday|thursay|thursady)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=TH)
        elif re.search(r'(friday|froday|fri)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=FR)
        elif re.search(r'(saturday|satuday|saturady|saterday|saturaday|saturdy|staurday|satuarday|sturday|satuerday|saurday|sat)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=SA)
        elif re.search(r'(sunday|sun)', match.group(), flags=re.IGNORECASE):
            pregnancy_end_date = date + relativedelta(weekday=SU)

        if pregnancy_end_date == date:
            pregnancy_end_date = pregnancy_end_date + relativedelta(days=7)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date = pregnancy_start_date + relativedelta(weeks=40)
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [59a] my due date is [name of the month] [day of the month]
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*(on\W*)?(january|janurary|jaunary|janaury|januray|janruary|jan|february|febraury|febuary|febrary|februrary|feburary|feburay|februay|feb|march|mar|april|apr|may|june|jun|july|jul|august|agust|augst|augest|auguest|aug|september|setember|septemer|septemeber|sepetember|septmeber|spetember|sptember|septmber|sep|sept|october|oct|november|novemeber|novmber|novemebr|novemember|novenber|novermber|novemver|nov|december|dcember|decemer|decemember|decemeber|decmber|decmeber|dec)\W*([1-9]|[1-2][0-9]|3[0-1])(st|nd|rd|th)?\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        day = int(match_digits[0])
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        year = date.year

        if re.search(r'(january|janurary|jaunary|janaury|januray|janruary|jan)', match.group(), flags=re.IGNORECASE):
            month = 1
        elif re.search(r'(february|febraury|febuary|febrary|februrary|feburary|feburay|februay|feb)', match.group(), flags=re.IGNORECASE):
            month = 2
        elif re.search(r'(march|mar)', match.group(), flags=re.IGNORECASE):
            month = 3
        elif re.search(r'(april|apr)', tweet,flags=re.IGNORECASE):
            month = 4
        elif re.search(r'may', match.group(), flags=re.IGNORECASE):
            month = 5
        elif re.search(r'(june|jun)', match.group(), flags=re.IGNORECASE):
            month = 6
        elif re.search(r'(july|jul)', match.group(), flags=re.IGNORECASE):
            month = 7
        elif re.search(r'(august|agust|augst|augest|auguest|aug)', match.group(), flags=re.IGNORECASE):
            month = 8
        elif re.search(r'(september|setember|septemer|septemeber|sepetember|septmeber|spetember|sptember|septmber|sep|sept)', match.group(), flags=re.IGNORECASE):
            month = 9
        elif re.search(r'(october|oct)', match.group(), flags=re.IGNORECASE):
            month = 10
        elif re.search(r'(november|novemeber|novmber|novemebr|novemember|novenber|novermber|novemver|nov)', match.group(), flags=re.IGNORECASE):
            month = 11
        elif re.search(r'(december|dcember|decemer|decemember|decemeber|decmber|decmeber|dec)', match.group(), flags=re.IGNORECASE):
            month = 12

        pregnancy_end_date = (str(year) + '-' + str(month) + '-' + str(day))
        pregnancy_end_date = datetime.strptime(pregnancy_end_date, "%Y-%m-%d")
        if relativedelta(pregnancy_end_date, date).months * 30 + relativedelta(pregnancy_end_date, date).days < 0:
            pregnancy_end_date = pregnancy_end_date + relativedelta(years=1)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = datetime.strftime(pregnancy_end_date, "%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [59b] my due date is [number of the month] [day of the month]
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*(on\W*)?([1-9]|0[1-9]|1[0-2])\W+([1-9]|0[1-9]|[1-2][0-9]|3[0-1])\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        month = int(match_digits[0])
        day = int(match_digits[1])
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        year = date.year
        pregnancy_end_date = (str(year) + '-' + str(month) + '-' + str(day))
        pregnancy_end_date = datetime.strptime(pregnancy_end_date, "%Y-%m-%d")
        if relativedelta(pregnancy_end_date, date).months * 30 + relativedelta(pregnancy_end_date, date).days < 0:
            pregnancy_end_date = pregnancy_end_date + relativedelta(years=1)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = datetime.strftime(pregnancy_end_date, "%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [60a] i'm due [name of the month] [day of the month]...baby
    if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(january|janurary|jaunary|janaury|januray|janruary|jan|february|febraury|febuary|febrary|februrary|feburary|feburay|februay|feb|march|mar|april|apr|may|june|jun|july|jul|august|agust|augst|augest|auguest|aug|september|setember|septemer|septemeber|sepetember|septmeber|spetember|sptember|septmber|sep|sept|october|oct|november|novemeber|novmber|novemebr|novemember|novenber|novermber|novemver|nov|december|dcember|decemer|decemember|decemeber|decmber|decmeber|dec)\W*([1-9]|[1-2][0-9]|3[0-1])(st|nd|rd|th)?\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        day = int(match_digits[0])
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        year = date.year

        if re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(january|janurary|jaunary|janaury|januray|janruary|jan)', match.group(), flags=re.IGNORECASE):
            month = 1
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(february|febraury|febuary|febrary|februrary|feburary|feburay|februay|feb)', match.group(), flags=re.IGNORECASE):
            month = 2
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(march|mar)', match.group(), flags=re.IGNORECASE):
            month = 3
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(april|apr)', match.group(), flags=re.IGNORECASE):
            month = 4
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?may', match.group(), flags=re.IGNORECASE):
            month = 5
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(june|jun)', match.group(), flags=re.IGNORECASE):
            month = 6
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(july|jul)', match.group(), flags=re.IGNORECASE):
            month = 7
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(august|agust|augst|augest|auguest|aug)', match.group(), flags=re.IGNORECASE):
            month = 8
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(september|setember|septemer|septemeber|sepetember|septmeber|spetember|sptember|septmber|sep|sept)', match.group(), flags=re.IGNORECASE):
            month = 9
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(october|oct)', match.group(), flags=re.IGNORECASE):
            month = 10
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(november|novemeber|novmber|novemebr|novemember|novenber|novermber|novemver|nov)', match.group(), flags=re.IGNORECASE):
            month = 11
        elif re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(december|dcember|decemer|decemember|decemeber|decmber|decmeber|dec)', match.group(), flags=re.IGNORECASE):
            month = 12

        pregnancy_end_date = (str(year) + '-' + str(month) + '-' + str(day))
        pregnancy_end_date = datetime.strptime(pregnancy_end_date, "%Y-%m-%d")
        if relativedelta(pregnancy_end_date, date).months * 30 + relativedelta(pregnancy_end_date, date).days < 0:
            pregnancy_end_date = pregnancy_end_date + relativedelta(years=1)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = datetime.strftime(pregnancy_end_date, "%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [60b] i'm due [number of the month] [day of the month]...baby
    if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?([1-9]|0[1-9]|1[0-2])\W+([1-9]|0[1-9]|[1-2][0-9]|3[0-1])\b.*\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        month = int(match_digits[0])
        day = int(match_digits[1])
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        year = date.year
        pregnancy_end_date = (str(year) + '-' + str(month) + '-' + str(day))
        pregnancy_end_date = datetime.strptime(pregnancy_end_date, "%Y-%m-%d")
        if relativedelta(pregnancy_end_date, date).months * 30 + relativedelta(pregnancy_end_date, date).days < 0:
            pregnancy_end_date = pregnancy_end_date + relativedelta(years=1)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = datetime.strftime(pregnancy_end_date, "%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [61a] baby...i'm due [name of the month] [day of the month]
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(january|janurary|jaunary|janaury|januray|janruary|jan|february|febraury|febuary|febrary|februrary|feburary|feburay|februay|feb|march|mar|april|apr|may|june|jun|july|jul|august|agust|augst|augest|auguest|aug|september|setember|septemer|septemeber|sepetember|septmeber|spetember|sptember|septmber|sep|sept|october|oct|november|novemeber|novmber|novemebr|novemember|novenber|novermber|novemver|nov|december|dcember|decemer|decemember|decemeber|decmber|decmeber|dec)\W*([1-9]|[1-2][0-9]|3[0-1])(st|nd|rd|th)?\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?(january|janurary|jaunary|janaury|januray|janruary|jan|february|febraury|febuary|febrary|februrary|feburary|feburay|februay|feb|march|mar|april|apr|may|june|jun|july|jul|august|agust|augst|augest|auguest|aug|september|setember|septemer|septemeber|sepetember|septmeber|spetember|sptember|septmber|sep|sept|october|oct|november|novemeber|novmber|novemebr|novemember|novenber|novermber|novemver|nov|december|dcember|decemer|decemember|decemeber|decmber|decmeber|dec)\W*([1-9]|[1-2][0-9]|3[0-1])(st|nd|rd|th)?\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            day = int(match_digits[0])
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            year = date.year

            if re.search(r'(january|janurary|jaunary|janaury|januray|janruary|jan)', match.group(), flags=re.IGNORECASE):
                month = 1
            elif re.search(r'(february|febraury|febuary|febrary|februrary|feburary|feburay|februay|feb)', match.group(), flags=re.IGNORECASE):
                month = 2
            elif re.search(r'(march|mar)', match.group(), flags=re.IGNORECASE):
                month = 3
            elif re.search(r'(april|apr)', match.group(), flags=re.IGNORECASE):
                month = 4
            elif re.search(r'may', match.group(), flags=re.IGNORECASE):
                month = 5
            elif re.search(r'(june|jun)', match.group(), flags=re.IGNORECASE):
                month = 6
            elif re.search(r'(july|jul)', match.group(), flags=re.IGNORECASE):
                month = 7
            elif re.search(r'(august|agust|augst|augest|auguest|aug)', match.group(), flags=re.IGNORECASE):
                month = 8
            elif re.search(r'(september|setember|septemer|septemeber|sepetember|septmeber|spetember|sptember|septmber|sep|sept)', match.group(), flags=re.IGNORECASE):
                month = 9
            elif re.search(r'(october|oct)', match.group(), flags=re.IGNORECASE):
                month = 10
            elif re.search(r'(november|novemeber|novmber|novemebr|novemember|novenber|novermber|novemver|nov)', match.group(), flags=re.IGNORECASE):
                month = 11
            elif re.search(r'(december|dcember|decemer|decemember|decemeber|decmber|decmeber|dec)', match.group(), flags=re.IGNORECASE):
                month = 12

            pregnancy_end_date = (str(year) + '-' + str(month) + '-' + str(day))
            pregnancy_end_date = datetime.strptime(pregnancy_end_date, "%Y-%m-%d")
            if relativedelta(pregnancy_end_date, date).months * 30 + relativedelta(pregnancy_end_date, date).days < 0:
                pregnancy_end_date = pregnancy_end_date + relativedelta(years=1)
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = datetime.strftime(pregnancy_end_date, "%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [61b] baby...i'm due [number of the month] [day of the month]
    if re.search(r'\b(pregnant|prgnt|pregnt|prgnant|preg|pregs|pregg|preggs|prego|pregos|preggo|preggos|pregger|preggers|preger|pregers|preganant|pregnanat|pregannt|pegnant|pregent|oregnant|pregrant|prgenant|pergant|pregnnt|preganat|prengnant|prenant|pregnnat|pergnant|pragnant|pregnate|pregnan|pregnatn|pregnante|pregnent|pregnet|preagnant|pregnat|prengant|pregant|pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct|bump|babybump|baby|babyboy|babygirl|belly)\b.*(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?([1-9]|0[1-9]|1[0-2])\W+([1-9]|0[1-9]|[1-2][0-9]|3[0-1])\b', tweet, flags=re.IGNORECASE):

        if match := re.search(r'(?<!like\W)(?<!if\W)\bi(\s*am|\W*m)\W*due\W*(on\W*)?([1-9]|0[1-9]|1[0-2])\W+([1-9]|0[1-9]|[1-2][0-9]|3[0-1])\b', tweet, flags=re.IGNORECASE):

            match_digits = regex_digits.findall(match.group())
            month = int(match_digits[0])
            day = int(match_digits[1])
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            year = date.year
            pregnancy_end_date = (str(year) + '-' + str(month) + '-' + str(day))
            pregnancy_end_date = datetime.strptime(pregnancy_end_date, "%Y-%m-%d")
            if relativedelta(pregnancy_end_date, date).months * 30 + relativedelta(pregnancy_end_date, date).days < 0:
                pregnancy_end_date = pregnancy_end_date + relativedelta(years=1)
            pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
            pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
            pregnancy_end_date_formatted = datetime.strftime(pregnancy_end_date, "%Y-%m-%d")
            pattern = match.re.pattern

            return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [62a] [name of the month] [day of the month] is my due date
    if match := re.search(r'(?<!like\W)(?<!if\W)\b(january|janurary|jaunary|janaury|januray|janruary|jan|february|febraury|febuary|febrary|februrary|feburary|feburay|februay|feb|march|mar|april|apr|may|june|jun|july|jul|august|agust|augst|augest|auguest|aug|september|setember|septemer|septemeber|sepetember|septmeber|spetember|sptember|septmber|sep|sept|october|oct|november|novemeber|novmber|novemebr|novemember|novenber|novermber|novemver|nov|december|dcember|decemer|decemember|decemeber|decmber|decmeber|dec)\W*([1-9]|[1-2][0-9]|3[0-1])\W*((st|nd|rd|th)\W*)?is\W*my\W*due\W*date\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        day = int(match_digits[0])
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        year = date.year

        if re.search(r'(january|janurary|jaunary|janaury|januray|janruary|jan)', match.group(), flags=re.IGNORECASE):
            month = 1
        elif re.search(r'(february|febraury|febuary|febrary|februrary|feburary|feburay|februay|feb)', match.group(), flags=re.IGNORECASE):
            month = 2
        elif re.search(r'(march|mar)', match.group(), flags=re.IGNORECASE):
            month = 3
        elif re.search(r'(april|apr)', match.group(), flags=re.IGNORECASE):
            month = 4
        elif re.search(r'may', match.group(), flags=re.IGNORECASE):
            month = 5
        elif re.search(r'(june|jun)', match.group(), flags=re.IGNORECASE):
            month = 6
        elif re.search(r'(uly|jul)', match.group(), flags=re.IGNORECASE):
            month = 7
        elif re.search(r'(august|agust|augst|augest|auguest|aug)', match.group(), flags=re.IGNORECASE):
            month = 8
        elif re.search(r'(september|setember|septemer|septemeber|sepetember|septmeber|spetember|sptember|septmber|sep|sept)', match.group(), flags=re.IGNORECASE):
            month = 9
        elif re.search(r'(october|oct)', match.group(), flags=re.IGNORECASE):
            month = 10
        elif re.search(r'(november|novemeber|novmber|novemebr|novemember|novenber|novermber|novemver|nov)', match.group(), flags=re.IGNORECASE):
            month = 11
        elif re.search(r'(december|dcember|decemer|decemember|decemeber|decmber|decmeber|dec)', match.group(), flags=re.IGNORECASE):
            month = 12

        pregnancy_end_date = (str(year) + '-' + str(month) + '-' + str(day))
        pregnancy_end_date = datetime.strptime(pregnancy_end_date, "%Y-%m-%d")
        if relativedelta(pregnancy_end_date, date).months * 30 + relativedelta(pregnancy_end_date, date).days < 0:
            pregnancy_end_date = pregnancy_end_date + relativedelta(years=1)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = datetime.strftime(pregnancy_end_date, "%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [62b] [number of the month] [day of the month] is my due date
    if match := re.search(r'(?<!like\W)(?<!if\W)\b([1-9]|0[1-9]|1[0-2])\W+([1-9]|0[1-9]|[1-2][0-9]|3[0-1])\W*is\W*my\W*due\W*date\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        month = int(match_digits[0])
        day = int(match_digits[1])
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        year = date.year
        pregnancy_end_date = (str(year) + '-' + str(month) + '-' + str(day))
        pregnancy_end_date = datetime.strptime(pregnancy_end_date, "%Y-%m-%d")
        if relativedelta(pregnancy_end_date, date).months * 30 + relativedelta(pregnancy_end_date, date).days < 0:
            pregnancy_end_date = pregnancy_end_date + relativedelta(years=1)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = datetime.strftime(pregnancy_end_date, "%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [63a] my due date is the [day of the month] [name of the month]
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*(on\W*)?\W*the\W*([1-9]|[1-2][0-9]|3[0-1])\W*((st|nd|rd|th)\W*)?of\W*(january|janurary|jaunary|janaury|januray|janruary|jan|february|febraury|febuary|febrary|februrary|feburary|feburay|februay|feb|march|mar|april|apr|may|june|jun|july|jul|august|agust|augst|augest|auguest|aug|september|setember|septemer|septemeber|sepetember|septmeber|spetember|sptember|septmber|sep|sept|october|oct|november|novemeber|novmber|novemebr|novemember|novenber|novermber|novemver|nov|december|dcember|decemer|decemember|decemeber|decmber|decmeber|dec)\b',
tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        day = int(match_digits[0])
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        year = date.year

        if re.search(r'(january|janurary|jaunary|janaury|januray|janruary|jan)', match.group(), flags=re.IGNORECASE):
            month = 1
        elif re.search(r'(february|febraury|febuary|febrary|februrary|feburary|feburay|februay|feb)', match.group(), flags=re.IGNORECASE):
            month = 2
        elif re.search(r'(march|mar)', match.group(), flags=re.IGNORECASE):
            month = 3
        elif re.search(r'(april|apr)', match.group(), flags=re.IGNORECASE):
            month = 4
        elif re.search(r'may', match.group(), flags=re.IGNORECASE):
            month = 5
        elif re.search(r'(june|jun)', match.group(), flags=re.IGNORECASE):
            month = 6
        elif re.search(r'(july|jul)', match.group(), flags=re.IGNORECASE):
            month = 7
        elif re.search(r'(august|agust|augst|augest|auguest|aug)', match.group(), flags=re.IGNORECASE):
            month = 8
        elif re.search(r'(september|setember|septemer|septemeber|sepetember|septmeber|spetember|sptember|septmber|sep|sept)', match.group(), flags=re.IGNORECASE):
            month = 9
        elif re.search(r'(october|oct)', match.group(), flags=re.IGNORECASE):
            month = 10
        elif re.search(r'(november|novemeber|novmber|novemebr|novemember|novenber|novermber|novemver|nov)', match.group(), flags=re.IGNORECASE):
            month = 11
        elif re.search(r'(december|dcember|decemer|decemember|decemeber|decmber|decmeber|dec)', match.group(), flags=re.IGNORECASE):
            month = 12

        pregnancy_end_date = (str(year) + '-' + str(month) + '-' + str(day))
        pregnancy_end_date = datetime.strptime(pregnancy_end_date, "%Y-%m-%d")
        if relativedelta(pregnancy_end_date, date).months * 30 + relativedelta(pregnancy_end_date, date).days < 0:
            pregnancy_end_date = pregnancy_end_date + relativedelta(years=1)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = datetime.strftime(pregnancy_end_date, "%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [63b] my due date is the [day of the month]
    if match := re.search(r'(?<!like\W)(?<!if\W)\bmy\W*due\W*date\W*(is|s)\W*(on\W*)?\W*the\W*([1-9]|[1-2][0-9]|3[0-1])(st|nd|rd|th)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        day = int(match_digits[0])
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        month = date.month
        year = date.year
        pregnancy_end_date = (str(year) + '-' + str(month) + '-' + str(day))
        pregnancy_end_date = datetime.strptime(pregnancy_end_date, "%Y-%m-%d")
        if relativedelta(pregnancy_end_date, date).months * 30 + relativedelta(pregnancy_end_date, date).days < 0:
            pregnancy_end_date = pregnancy_end_date + relativedelta(years=1)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = datetime.strftime(pregnancy_end_date, "%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [64] i'm halfway through my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*am|\W*m)\W*(?!not)([a-z]+\W*)?half\W*way\W*(through|thru|over|done|finished|in\W*to|along\W*in)\W*((with|w)\W*)?((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + relativedelta(weeks=20)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [65] my pregnancy is halfway
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bmy\W*(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\W*(is|s)\W*(half|halfway)\b', tweet, flags=re.IGNORECASE):

        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + relativedelta(weeks=20)
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [66] i have months left in my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*have|\W*ve|\s*have\s*got|\W*ve\s*got)\W*(([a-z]+|less\W*than)\W*)?([1-5]|a|one|two|three|four|five|a\W*couple|a\W*couple\W*of|a\W*few)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)\W*(left|to\W*go|left\W*to\W*go)\W*in\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        delta = relativedelta(months=quantity_months)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [67] i have weeks left in my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*have|\W*ve|\s*have\s*got|\W*ve\s*got)\W*(([a-z]+|less\W*than)\W*)?([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(left|to\W*go|left\W*to\W*go)\W*in\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        delta = relativedelta(weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [68] i have days left in my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*have|\W*ve|\s*have\s*got|\W*ve\s*got)\W*([a-z]+\W*)?([1-9]|[1-9][0-9]|100|a|one|two|three|four|five|six|seven|eight|nine|ten|a\W*couple|a\W*couple\W*of|a\W*few)\W*(dayd|dyas|days|day)\W*(left|to\W*go|left\W*to\W*go)\W*in\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_days = int(match_digits[0])
        delta = relativedelta(days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [69] i have months and weeks left in my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*have|\W*ve|\s*have\s*got|\W*ve\s*got)\W*([a-z]+\W*)?([1-5]|a|one|two|three|four|five)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(left|to\W*go|left\W*to\W*go)\W*in\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        delta = relativedelta(months=quantity_months,weeks=quantity_weeks)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [70] i have months and days left in my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*have|\W*ve|\s*have\s*got|\W*ve\s*got)\W*([a-z]+\W*)?([1-5]|a|one|two|three|four|five)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|[1-9][0-9]|100|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(dayd|dyas|days|day)\W*(left|to\W*go|left\W*to\W*go)\W*in\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(months=quantity_months,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [71] i have months, weeks, and days left in my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*have|\W*ve|\s*have\s*got|\W*ve\s*got)\W*([a-z]+\W*)?([1-5]|a|one|two|three|four|five)\W*(months|month|m|mo|mnth|mnths|mths|monts|mounths|monnths|montsh|monhts|mpnths|nonths|mionths|monrhs|montrh|minth|mounth|monthss|onths|montyhs|monh|montha|onth|monthd|monthe|montths|moonths|monhs|omnths|mnoths|mth|motnh|moinths|moth|minths|motnhs|monthes|momth|moths|mobths|motnsh|momths|mothes|mmonths|mos)(and|\W|amp)*([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(and|\W|amp)*([1-9]|[1-9][0-9]|100|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(dayd|dyas|days|day)\W*(left|to\W*go|left\W*to\W*go)\W*in\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_months = int(match_digits[0])
        quantity_weeks = int(match_digits[1])
        quantity_days = int(match_digits[2])
        delta = relativedelta(months=quantity_months,weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    # [72] i have weeks and days left in my pregnancy
    if match := re.search(r'(?<!untill\W)(?<!unil\W)(?<!untili\W)(?<!till\W)(?<!ubtil\W)(?<!unitl\W)(?<!untll\W)(?<!until\W)(?<!til\W)(?<!intil\W)(?<!unttil\W)(?<!intill\W)(?<!unti\W)(?<!unill\W)(?<!untl\W)(?<!untiil\W)(?<!ntil\W)(?<!untii\W)(?<!till\W)(?<!til\W)(?<!like\W)(?<!if\W)(?<!when\W)\bi(\s*have|\W*ve|\s*have\s*got|\W*ve\s*got)\W*([a-z]+\W*)?([1-9]|1[0-9]|20|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(week|wweks|weks|wek|wekks|weeeks|wk|weekd|wekk|weeek|weeka|weekss|weeks|wks|wweeks|w)\W*(and|\W|amp)*([1-9]|[1-9][0-9]|100|a|one|two|three|four|five|six|seven|eight|nine|ten)\W*(dayd|dyas|days|day)\W*(left|to\W*go|left\W*to\W*go)\W*in\W*((my|this)\W*)?(pregnancy|pregnance|pregnanacy|pregnency|regnancy|pregnancie|pregnantcy|pregancy|pregnancey|pragnancy|preganacy|prenancy|pregnncy|pregnacy|pegnancy|preganancy|pregnany|prengnancy|preganncy|pregency|pregnnacy|pregy|preggy|prengnacy|prgnancy|pregnanct)\b', tweet, flags=re.IGNORECASE):

        match_digits = regex_digits.findall(match.group())
        quantity_weeks = int(match_digits[0])
        quantity_days = int(match_digits[1])
        delta = relativedelta(weeks=quantity_weeks,days=quantity_days)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pregnancy_end_date = date + delta
        pregnancy_start_date = pregnancy_end_date - relativedelta(weeks=40)
        pregnancy_start_date_formatted = pregnancy_start_date.strftime("%Y-%m-%d")
        pregnancy_end_date_formatted = pregnancy_end_date.strftime("%Y-%m-%d")
        pattern = match.re.pattern

        return pregnancy_start_date_formatted, pregnancy_end_date_formatted, pattern

    return 0, 0, 0


if __name__ == "__main__":
    tweets = pd.read_csv("development_tweets.tsv", delimiter='\t')
    preg_start_date = []
    preg_end_date = []
    pattern_tweet = []
    for row_index, row in tweets.iterrows():

        # Input = original tweet
        #pregnancy_start_date, pregnancy_end_date = extract_pregnancy_timeframe(row['text'], row['created_at'])

        # Input = pre-processed tweet
        pregnancy_start_date, pregnancy_end_date, pattern = extract_pregnancy_timeframe(preprocess(row['text']), row['created_at'])

        preg_start_date.append(pregnancy_start_date)
        preg_end_date.append(pregnancy_end_date)
        pattern_tweet.append(pattern)

        if pregnancy_start_date:
            # Prints with original tweet
            print(row['text'], row['created_at'], pregnancy_start_date, pregnancy_end_date, pattern)

            # Prints with pre-processed tweet
            # print(preprocess(row['text']), row['created_at'], pregnancy_start_date, pregnancy_end_date)

    tweets['pregnancy_start_date'] = preg_start_date
    tweets['pregnancy_end_date'] = preg_end_date
    #tweets['pattern'] = pattern_tweet
    tweets.drop(tweets[tweets['pregnancy_start_date'] == 0].index, inplace=True)
    tweets.to_csv('pregnancy_timeframes.tsv', index=False, header=True, sep='\t')