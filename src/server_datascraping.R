# if (!"rvest" %in% installed.packages()) install.packages("rvest")
# if (!"plyr" %in% installed.packages()) install.packages("plyr")
# if (!"dplyr" %in% installed.packages()) install.packages("dplyr")
# if (!"stringr" %in% installed.packages()) install.packages("stringr")
# if (!"httr" %in% installed.packages()) install.packages("httr")
# if (!"RCurl" %in% installed.packages()) install.packages("RCurl")
# if (!"zoo" %in% installed.packages()) install.packages("zoo")
# if (!"pystr" %in% installed.packages()) install.packages("pystr")

library(rvest); library(plyr); library(dplyr); library(stringr); library(httr); library(RCurl); library(zoo); library(pystr); library(foreach); library(doParallel)

workdir = "/home/pareenj/Ballroom"
setwd(workdir)

domain = "http://www.worlddancesport.org"

# url_calendar13 = "http://www.worlddancesport.org/Calendar/Competition/Any#format=List&month=0&year=2013&TypeFilter=171,170,173,169,187,188,202,189,203,192,204,193,194,174,172,178,176,179,180,184,190,210,197,191,211,181,186,209,183,207,208,206,205,185,182,201&disciplineFilter=56,59,61,76,77,78,79,80,55,60,63,81,82,83,84,85,57,64,65,68,70,71,86,87,88,89,90,66,91,92,93,94,172,95,99,138,145,152,103,104,105,106,108,67,109,110,111&ageGroupFilter=180,186,179,190,185,177,178,184,181,194,182,183,196,205,206,187,175,176&countryFilter=-1&nameFilter=&kindFilter=Competition"
# url_calendar14 = "http://www.worlddancesport.org/Calendar/Competition/Any#format=List&month=0&year=2014&TypeFilter=171,170,173,169,187,188,202,189,203,192,204,193,194,174,172,178,176,179,180,184,190,210,197,191,211,181,186,209,183,207,208,206,205,185,182,201&disciplineFilter=56,59,61,76,77,78,79,80,55,60,63,81,82,83,84,85,57,64,65,68,70,71,86,87,88,89,90,66,91,92,93,94,172,95,99,138,145,152,103,104,105,106,108,67,109,110,111&ageGroupFilter=180,186,179,190,185,177,178,184,181,194,182,183,196,205,206,187,175,176&countryFilter=-1&nameFilter=&kindFilter=Competition"
# url_calendar15 = "http://www.worlddancesport.org/Calendar/Competition/Any#format=List&month=0&year=2015&TypeFilter=171,170,173,169,187,188,202,189,203,192,204,193,194,174,172,178,176,179,180,184,190,210,197,191,211,181,186,209,183,207,208,206,205,185,182,201&disciplineFilter=56,59,61,76,77,78,79,80,55,60,63,81,82,83,84,85,57,64,65,68,70,71,86,87,88,89,90,66,91,92,93,94,172,95,99,138,145,152,103,104,105,106,108,67,109,110,111&ageGroupFilter=180,186,179,190,185,177,178,184,181,194,182,183,196,205,206,187,175,176&countryFilter=-1&nameFilter=&kindFilter=Competition"
# url_calendar16 = "http://www.worlddancesport.org/Calendar/Competition/Any#format=List&month=0&year=2016&TypeFilter=171,170,173,169,187,188,202,189,203,192,204,193,194,174,172,178,176,179,180,184,190,210,197,191,211,181,186,209,183,207,208,206,205,185,182,201&disciplineFilter=56,59,61,76,77,78,79,80,55,60,63,81,82,83,84,85,57,64,65,68,70,71,86,87,88,89,90,66,91,92,93,94,172,95,99,138,145,152,103,104,105,106,108,67,109,110,111&ageGroupFilter=180,186,179,190,185,177,178,184,181,194,182,183,196,205,206,187,175,176&countryFilter=-1&nameFilter=&kindFilter=Competition"
# download.file(url_calendar13, destfile = "Calendar 2013.html")
# download.file(url_calendar14, destfile = "Calendar 2014.html")
# download.file(url_calendar15, destfile = "Calendar 2015.html")
# download.file(url_calendar16, destfile = "Calendar 2016.html")

html_calendar13 = read_html("Calendar 2013.html")
html_calendar14 = read_html("Calendar 2014.html")
html_calendar15 = read_html("Calendar 2015.html")
html_calendar16 = read_html("Calendar 2016.html")

# html_calendars = vector(length = 4)
# html_calendars[1] = html_calendar13
# html_calendars[2] = html_calendar14
# html_calendars[3] = html_calendar15

date_13 = html_calendar13 %>% html_nodes(css = "td:nth-child(2)") %>% html_text() %>% as.Date(format = "%d/%m/%Y")
name_13 = html_calendar13 %>% html_nodes(css = "td:nth-child(3)") %>% html_text()
agegroup_13 = html_calendar13 %>% html_nodes(css = "td:nth-child(4)") %>% html_text()
discipline_13 = html_calendar13 %>% html_nodes(css = "td:nth-child(5)") %>% html_text()
location_13 = html_calendar13 %>% html_nodes(css = "td:nth-child(6)") %>% html_text()
country_13 = html_calendar13 %>% html_nodes(css = "td:nth-child(7)") %>% html_text()
info_13 = html_calendar13 %>% html_nodes(css = "td:nth-child(8)") %>% html_text()
rankings_url_13 = html_calendar13 %>% html_nodes(css = "td a") %>% html_attr("href")

date_14 = html_calendar14 %>% html_nodes(css = "td:nth-child(2)") %>% html_text() %>% as.Date(format = "%d/%m/%Y")
name_14 = html_calendar14 %>% html_nodes(css = "td:nth-child(3)") %>% html_text()
agegroup_14 = html_calendar14 %>% html_nodes(css = "td:nth-child(4)") %>% html_text()
discipline_14 = html_calendar14 %>% html_nodes(css = "td:nth-child(5)") %>% html_text()
location_14 = html_calendar14 %>% html_nodes(css = "td:nth-child(6)") %>% html_text()
country_14 = html_calendar14 %>% html_nodes(css = "td:nth-child(7)") %>% html_text()
info_14 = html_calendar14 %>% html_nodes(css = "td:nth-child(8)") %>% html_text()
rankings_url_14 = html_calendar14 %>% html_nodes(css = "td a") %>% html_attr("href")

date_15 = html_calendar15 %>% html_nodes(css = "td:nth-child(2)") %>% html_text() %>% as.Date(format = "%d/%m/%Y")
name_15 = html_calendar15 %>% html_nodes(css = "td:nth-child(3)") %>% html_text()
agegroup_15 = html_calendar15 %>% html_nodes(css = "td:nth-child(4)") %>% html_text()
discipline_15 = html_calendar15 %>% html_nodes(css = "td:nth-child(5)") %>% html_text()
location_15 = html_calendar15 %>% html_nodes(css = "td:nth-child(6)") %>% html_text()
country_15 = html_calendar15 %>% html_nodes(css = "td:nth-child(7)") %>% html_text()
info_15 = html_calendar15 %>% html_nodes(css = "td:nth-child(8)") %>% html_text()
rankings_url_15 = html_calendar15 %>% html_nodes(css = "td a") %>% html_attr("href")

date_16 = html_calendar16 %>% html_nodes(css = "td:nth-child(2)") %>% html_text() %>% as.Date(format = "%d/%m/%Y")
name_16 = html_calendar16 %>% html_nodes(css = "td:nth-child(3)") %>% html_text()
agegroup_16 = html_calendar16 %>% html_nodes(css = "td:nth-child(4)") %>% html_text()
discipline_16 = html_calendar16 %>% html_nodes(css = "td:nth-child(5)") %>% html_text()
location_16 = html_calendar16 %>% html_nodes(css = "td:nth-child(6)") %>% html_text()
country_16 = html_calendar16 %>% html_nodes(css = "td:nth-child(7)") %>% html_text()
info_16 = html_calendar16 %>% html_nodes(css = "td:nth-child(8)") %>% html_text()
rankings_url_16 = html_calendar16 %>% html_nodes(css = "td a") %>% html_attr("href")

event_date = c(date_13, date_14, date_15, date_16)
event_name = c(name_13, name_14, name_15, name_16) %>% as.factor()
event_agegroup = c(agegroup_13, agegroup_14, agegroup_15, agegroup_16) %>% as.factor()
event_discipline = c(discipline_13, discipline_14, discipline_15, discipline_16) %>% as.factor()
event_location = c(location_13, location_14, location_15, location_16) %>% as.factor()
event_country = c(country_13, country_14, country_15, country_16) %>% as.factor()
event_info = c(info_13, info_14, info_15, info_16) %>% as.factor()
event_rankings_url = c(rankings_url_13, rankings_url_14, rankings_url_15, rankings_url_16)

Event = data.frame(event_name, event_date, event_agegroup, event_discipline, event_location, event_country, event_rankings_url, event_info)
Event = subset(Event, Event$event_info == "Results")
Event$event_rankings_url = as.character(Event$event_rankings_url); event_urls = Event$event_rankings_url
event_id = 1:nrow(Event)
Event = data.frame(event_id, Event)
write.csv(Event, "Event.csv", row.names = FALSE)

####################################################################################################################
extract = function(couple_html, string)
{
  text_vector = couple_html %>% html_nodes(css = "dt") %>% html_text()
  index = grep(string, text_vector)
  required_value = couple_html %>% html_nodes(css = paste0("dd:nth-child(", 2*index ,")")) %>% html_text()
  required_value = gsub("\r", "", gsub("\n", "", gsub("  ", "", required_value)))
  return(required_value)
}
####################################################################################################################

Placements = data.frame()
Couples = data.frame()
Athletes = data.frame()
Rounds = data.frame()
Judges = data.frame()
MarksNonFinal = data.frame()
MarksFinal = data.frame()

cl = makeCluster(detectCores())
registerDoParallel(cl)

for(i in 1:length(event_id))
{
  tryCatch(
    {
      cat(i, "out of 4065", "\n")
      if((i %% 25) == 0) Sys.sleep(runif(1, min = 5, max = 10))
      ## sum(grepl("/Ranking$", event_urls)) == events_number
      
      event_i_rankings_html = read_html(event_urls[i])
      # event_i_name = event_i_rankings_html %>% html_nodes(css = "#breadcrumbs a:nth-child(5)") %>% html_text()
      # dir.create(file.path(workdir, event_i_name))
      # setwd(file.path(workdir, event_i_name))
      # download.file(event_urls[i], "Rankings.html")
      
      event_i_couple_placement = event_i_rankings_html %>% html_nodes(css = "td.rank") %>% html_text()
      event_i_event_id = rep(i, length(event_i_couple_placement))
      event_i_couple_url = event_i_rankings_html %>% html_nodes(css = "td.rank a") %>% html_attr("href")
      event_i_couple_country = event_i_rankings_html %>% html_nodes(css = ".rank~ td:nth-child(3)") %>% html_text()
      event_i_couple_number = event_i_rankings_html %>% html_nodes(css = ".rank~ td:nth-child(4)") %>% html_text()
      event_i_couple_id = gsub("/Couple/Detail/", replacement = "", x = event_i_couple_url)
      event_i_couple_url = paste0(domain, event_i_couple_url)
      
      event_i_placement = data.frame(event_id = event_i_event_id, couple_id = event_i_couple_id, couple_placement = event_i_couple_placement, couple_number = event_i_couple_number)
      if(nrow(Placements) == 0)
      {
        Placements = rbind(Placements, event_i_placement)
        write.csv(x = Placements, file = "Placements.csv", row.names = FALSE)
      } else {
        write.table(x = event_i_placement, file = "Placements.csv", append = TRUE, sep = ",", row.names = FALSE, col.names = FALSE)
      }
      cat("Placements updated\n")
      
      event_i_couple_id_new = c()
      event_i_couple_country_new = c()
      event_i_couple_joindate = c()
      event_i_couple_agegroup = c()
      event_i_couple_status = c()
      event_i_couple_division = c()
      event_i_couple_athlete_memberid_male = c()
      event_i_couple_athlete_memberid_female = c()
      
      for(j in 1:length(event_i_couple_id))
      {
        if(!(event_i_couple_id[j] %in% Couples$couple_id))
        {
          couple_ij_id = event_i_couple_id[j]
          couple_ij_country = event_i_couple_country[j]
          couple_ij_url = event_i_couple_url[j]
          couple_ij_html = read_html(couple_ij_url)
          couple_ij_joindate = couple_ij_html %>% extract("Joined on")
          couple_ij_agegroup = couple_ij_html %>% extract("Current age group")
          couple_ij_status = couple_ij_html %>% extract("Current status")
          couple_ij_division = couple_ij_html %>% extract("Division")
          #couple_ij_worldranking
          couple_ij_male = couple_ij_html %>% html_nodes(css = "dd:nth-child(2)") %>% html_text()
          couple_ij_athlete_memberid_male = as.integer(gsub("[^0-9]", "", couple_ij_male))
          couple_ij_male_url = couple_ij_html %>% html_nodes(css = "dd:nth-child(2) a") %>% html_attr("href")
          couple_ij_male_url = paste0(domain, couple_ij_male_url)
          couple_ij_female = couple_ij_html %>% html_nodes(css = "dd:nth-child(4)") %>% html_text()
          couple_ij_athlete_memberid_female = as.integer(gsub("[^0-9]", "", couple_ij_female))
          couple_ij_female_url = couple_ij_html %>% html_nodes(css = "dd:nth-child(4) a") %>% html_attr("href")
          couple_ij_female_url = paste0(domain, couple_ij_female_url)
          
          event_i_couple_id_new = c(event_i_couple_id_new, couple_ij_id)
          event_i_couple_country_new = c(event_i_couple_country_new, couple_ij_country)
          event_i_couple_joindate = c(event_i_couple_joindate, couple_ij_joindate)
          event_i_couple_agegroup = c(event_i_couple_agegroup, couple_ij_agegroup)
          event_i_couple_status = c(event_i_couple_status, couple_ij_status)
          event_i_couple_division = c(event_i_couple_division, couple_ij_division)
          event_i_couple_athlete_memberid_male = c(event_i_couple_athlete_memberid_male, couple_ij_athlete_memberid_male)
          event_i_couple_athlete_memberid_female = c(event_i_couple_athlete_memberid_female, couple_ij_athlete_memberid_female)
          
          Sys.sleep(1)
          
          if(!(couple_ij_athlete_memberid_male %in% Athletes$athlete_memberid))
          {
            athlete_ij_male_html = read_html(couple_ij_male_url)
            athlete_ij_male_id = couple_ij_athlete_memberid_male
            athlete_ij_male_name = athlete_ij_male_html %>% extract("Name")
            athlete_ij_male_surname = athlete_ij_male_html %>% extract("Surname")
            athlete_ij_male_nationality = athlete_ij_male_html %>% extract("Nationality")
            athlete_ij_male_memberof = athlete_ij_male_html %>% extract("Member of")
            athlete_ij_male_agegroup = athlete_ij_male_html %>% extract("Current age group")
            athlete_ij_male_division = ((athlete_ij_male_html %>% extract("Licenses") %>% strsplit("Division:"))[[1]][2] %>% strsplit("Status:"))[[1]][1]
            athlete_ij_male_status = ((athlete_ij_male_html %>% extract("Licenses") %>% strsplit("Division:"))[[1]][2] %>% strsplit("Status:"))[[1]][2]
            athlete_ij_male_sex = "Male"
            
            athlete_ij_male = data.frame(athlete_memberid = athlete_ij_male_id, athlete_name = athlete_ij_male_name, athlete_surname = athlete_ij_male_surname, athlete_sex = athlete_ij_male_sex, athlete_nationality = athlete_ij_male_nationality, athlete_agegroup = athlete_ij_male_agegroup, athlete_division = athlete_ij_male_division, athlete_status = athlete_ij_male_status)#, athlete_memberof = athlete_ij_male_memberof
            if(nrow(Athletes) == 0)
            {
              Athletes = rbind(Athletes, athlete_ij_male)
              write.csv(x = Athletes, file = "Athletes.csv", row.names = FALSE)
            }  else  {
              write.table(x = athlete_ij_male, file = "Athletes.csv", append = TRUE, sep = ",", row.names = FALSE, col.names = FALSE)
            }
            
            Sys.sleep(1)
          }
          
          if(!(couple_ij_athlete_memberid_female %in% Athletes$athlete_memberid))
          {
            athlete_ij_female_html = read_html(couple_ij_female_url)
            athlete_ij_female_id = couple_ij_athlete_memberid_female
            athlete_ij_female_name = athlete_ij_female_html %>% extract("Name")
            athlete_ij_female_surname = athlete_ij_female_html %>% extract("Surname")
            athlete_ij_female_nationality = athlete_ij_female_html %>% extract("Nationality")
            #athlete_ij_female_memberof = athlete_ij_female_html %>% extract("Member of")
            athlete_ij_female_agegroup = athlete_ij_female_html %>% extract("Current age group")
            athlete_ij_female_division = ((athlete_ij_female_html %>% extract("Licenses") %>% strsplit("Division:"))[[1]][2] %>% strsplit("Status:"))[[1]][1]
            athlete_ij_female_status = ((athlete_ij_female_html %>% extract("Licenses") %>% strsplit("Division:"))[[1]][2] %>% strsplit("Status:"))[[1]][2]
            athlete_ij_female_sex = "Female"
            
            athlete_ij_female = data.frame(athlete_memberid = athlete_ij_female_id, athlete_name = athlete_ij_female_name, athlete_surname = athlete_ij_female_surname, athlete_sex = athlete_ij_female_sex, athlete_nationality = athlete_ij_female_nationality, athlete_agegroup = athlete_ij_female_agegroup, athlete_division = athlete_ij_female_division, athlete_status = athlete_ij_female_status)#, athlete_memberof = athlete_ij_female_memberof
            write.table(x = athlete_ij_female, file = "Athletes.csv", append = TRUE, sep = ",", row.names = FALSE, col.names = FALSE)
            
            Sys.sleep(1)
          }
          Sys.sleep(1)
        }  else {
          j = j + 1
        }
        #rm(couple_ij_id, couple_ij_country, couple_ij_url, couple_ij_html, couple_ij_joindate, couple_ij_agegroup, couple_ij_status, couple_ij_division, couple_ij_male, couple_ij_athlete_memberid_male, couple_ij_male_url, couple_ij_female, couple_ij_athlete_memberid_female, couple_ij_female_url, athlete_ij_male_html, athlete_ij_male_id, athlete_ij_male_name, athlete_ij_male_surname, athlete_ij_male_nationality, athlete_ij_male_agegroup, athlete_ij_male_division, athlete_ij_male_status, athlete_ij_male_sex, athlete_ij_male, athlete_ij_female_html, athlete_ij_female_id, athlete_ij_female_name, athlete_ij_female_surname, athlete_ij_female_nationality, athlete_ij_female_agegroup, athlete_ij_female_division, athlete_ij_female_status, athlete_ij_female_sex, athlete_ij_female)#athlete_ij_male_memberof, athlete_ij_female_memberof
        gc()
      }
      cat("Athletes updated\n")
      
      event_i_couple = data.frame(couple_id = event_i_couple_id_new, couple_country = event_i_couple_country_new, couple_joindate = event_i_couple_joindate, couple_agegroup = event_i_couple_agegroup, couple_status = event_i_couple_status, couple_division = event_i_couple_division, athlete_memberid_male = event_i_couple_athlete_memberid_male, athlete_memberid_female = event_i_couple_athlete_memberid_female)
      if(nrow(Couples) == 0)
      {
        Couples = rbind(Couples, event_i_couple)
        write.csv(x = Couples, file = "Couples.csv", row.names = FALSE)
      } else  {
        write.table(x = event_i_couple, file = "Couples.csv", append = TRUE, sep = ",", row.names = FALSE, col.names = FALSE)
      }
      cat("Couples updated\n")
      
      event_i_info_url = gsub("/Ranking", "", event_urls[i])
      # download.file(event_i_info_url, "Event Information.html")
      event_i_info_html = read_html(event_i_info_url)
      
      event_i_round_round_name = event_i_info_html %>% html_nodes(css = "th+ th") %>% html_text()
      event_i_round_event_id = rep(i, length(event_i_round_round_name))
      event_i_round_couples_count = event_i_info_html %>% html_nodes(css = "tr:nth-child(1) td+ td") %>% html_text()
      #event_i_round_redance
      
      event_i_round = data.frame(round_name = event_i_round_round_name, couples_count = event_i_round_couples_count, event_id = event_i_round_event_id)
      if(nrow(Rounds) == 0)
      {
        Rounds = rbind(Rounds, event_i_round)
        write.csv(x = Rounds, file = "Rounds.csv", row.names = FALSE)
      } else  {
        write.table(x = event_i_round, file = "Rounds.csv", append = TRUE, sep = ",", row.names = FALSE, col.names = FALSE)
      }
      cat("Rounds updated\n")
      
      Sys.sleep(1)
      
      event_i_judges_url = paste0(event_i_info_url, "/Officials")
      # download.file(event_i_judges_url, "Officials.html")
      event_i_judges_html = read_html(event_i_judges_url)
      event_i_judges_name = event_i_judges_html %>% html_nodes(css = "thead+ tbody .name") %>% html_text()
      event_i_judges_url = event_i_judges_html %>% html_nodes(css = "thead+ tbody .name a") %>% html_attr("href")
      event_i_judges_id = gsub("/Official/Detail/", replacement = "", x = event_i_judges_url)
      event_i_judges_url = paste0(domain, event_i_judges_url)
      event_i_judges_country = event_i_judges_html %>% html_nodes(css = "thead+ tbody .name+ td") %>% html_text()
      event_i_judges_identifier = event_i_judges_html %>% html_nodes(css = "td:nth-child(3)") %>% html_text()
      
      Sys.sleep(1)
      
      for(k in 1:length(event_i_judges_id))
      {
        if(!(event_i_judges_id[k] %in% Judges$judge_id))
        {
          judge_ik_id = event_i_judges_id[k]
          judge_ik_url = event_i_judges_url[k]
          judge_ik_html = read_html(judge_ik_url)
          judge_ik_name = judge_ik_html %>% extract("Name")
          judge_ik_surname = judge_ik_html %>% extract("Surname")
          judge_ik_country = event_i_judges_country[k]
          judge_ik_nationality = judge_ik_html %>% extract("Nationality")
          judge_ik_memberid = judge_ik_html %>% extract("Member Id number")
          judge_ik_memberof = judge_ik_html %>% extract("Member of")
          judge_ik_license = judge_ik_html %>% extract("Licenses")
          
          judge_ik = data.frame(judge_id = judge_ik_id, judge_name = judge_ik_name, judge_surname = judge_ik_surname, judge_country = judge_ik_country, judge_nationality = judge_ik_nationality, judge_memberof = judge_ik_memberof, judge_license = judge_ik_license)
          if(nrow(Judges) == 0)
          {
            Judges = rbind(Judges, judge_ik)
            write.csv(x = Judges, file = "Judges.csv", row.names = FALSE)
          } else {
            write.table(x = judge_ik, file = "Judges.csv", append = TRUE, sep = ",", row.names = FALSE, col.names = FALSE)
          }
          Sys.sleep(1)
        }
        #rm(judge_ik_id, judge_ik_url, judge_ik_html, judge_ik_name, judge_ik_surname, judge_ik_country, judge_ik_nationality, judge_ik_memberid, judge_ik_memberof, judge_ik_license, judge_ik)
        gc()
      }
      cat("Judges updated\n")
      
      tryCatch(
        {
          event_i_marks_url = paste0(event_i_info_url, "/Marks")
          # download.file(event_i_marks_url, "Marks.html")
          if(url.exists(event_i_marks_url))
          {
            event_i_marks_html = read_html(event_i_marks_url)
            event_i_marks_dances = event_i_marks_html %>% html_nodes(css = "th+ .adjudicator") %>% html_text()
            event_i_marks_identifiers = event_i_marks_html %>% html_nodes(css = "th+ .ajud") %>% html_text()
            event_i_marks_unique_identifiers = unique(event_i_marks_identifiers)
            match_vector = match(event_i_marks_unique_identifiers, event_i_judges_identifier)
            event_i_marks_judges_id = event_i_judges_id[match_vector]
            
            event_i_marks_table = event_i_marks_html %>% html_nodes(css = "table") %>% html_table(fill = TRUE) %>% as.data.frame()
            event_i_marks_table$Var.1[event_i_marks_table$Var.1 == ""] = NA
            event_i_marks_table = event_i_marks_table[rowSums(is.na(event_i_marks_table)) != ncol(event_i_marks_table), ]
            row_shift = vector(); row_shift[1] = FALSE
            
            for(j in 2:nrow(event_i_marks_table))
            {
              row_shift[j] = is.na(as.numeric(event_i_marks_table$NA.[j]))
            }
            
            event_i_marks_table[row_shift, -(1:2)] = event_i_marks_table[row_shift, -c((ncol(event_i_marks_table)-1), ncol(event_i_marks_table))]
            
            for(j in 2:nrow(event_i_marks_table))
            {
              event_i_marks_table[row_shift, (1:2)] = ""
            }
            
            numberof_dances = length(event_i_marks_dances)
            numberof_judges = length(event_i_judges_name)
            
            col_names = as.character(as.vector(event_i_marks_table[1,]))
            
            for(j in 1:numberof_dances)
            {
              idx_1 = 4 + (j-1)*(numberof_judges + 1); idx_2 = 3 + j*(numberof_judges + 1)
              pref = colnames(event_i_marks_table)[idx_1]
              col_names[idx_1:idx_2] = paste0(pref, "_", col_names[idx_1:idx_2])
            }
            
            col_names[ncol(event_i_marks_table)] = colnames(event_i_marks_table)[ncol(event_i_marks_table)]
            colnames(event_i_marks_table) = col_names
            event_i_marks_table = event_i_marks_table[-1, ]
            if(sum(event_i_marks_table[,1] == "") != 0)
            {
              event_i_marks_table[which(event_i_marks_table[,1] == ""),][,1] = NA
              event_i_marks_table[which(event_i_marks_table[,2] == ""),][,2] = NA
              event_i_marks_table = transform(event_i_marks_table, Rank = na.locf(Rank), Couple = na.locf(Couple))
            }
            
            for(j in 4:(ncol(event_i_marks_table) - 1))
            {
              for(k in 1:nrow(event_i_marks_table))
              {
                mark_ijk_judge_identifier = (colnames(event_i_marks_table)[j] %>% strsplit("_") %>% unlist())[2]
                if(pystr_isalpha(mark_ijk_judge_identifier))
                {
                  mark_ijk_event_id = event_id[i]
                  mark_ijk_couple_id = event_i_couple_id[which(event_i_marks_table[k, 2] == event_i_couple_number)]
                  mark_ijk_roundname = event_i_marks_table[k, 3]
                  mark_ijk_mark_dance = (colnames(event_i_marks_table)[j] %>% strsplit("_") %>% unlist())[1]
                  mark_ijk_judge_id = event_i_judges_id[which(mark_ijk_judge_identifier == event_i_judges_identifier)]
                  mark_ijk_mark_given = event_i_marks_table[k,j]
                  
                  mark_ijk = data.frame(event_id = mark_ijk_event_id, round_name = mark_ijk_roundname, couple_id = mark_ijk_couple_id, mark_dance = mark_ijk_mark_dance, mark_given = mark_ijk_mark_given)
                  if(nrow(MarksNonFinal) == 0)
                  {
                    MarksNonFinal = rbind(MarksNonFinal, mark_ijk)
                    write.csv(x = MarksNonFinal, file = "MarksNonFinal.csv", row.names = FALSE)
                  } else  {
                    write.table(x = mark_ijk, file = "MarksNonFinal.csv", append = TRUE, sep = ",", row.names = FALSE, col.names = FALSE)
                  }
                }
              }
              #rm(mark_ijk_judge_identifier, mark_ijk_event_id, mark_ijk_couple_id, mark_ijk_roundname, mark_ijk_mark_dance, mark_ijk_judge_id, mark_ijk_mark_given, mark_ijk)
              gc()
            }
            cat("MarksNonFinal updated\n")
            Sys.sleep(1)
          }
          
        }, error = function(e){cat("Error: ", conditionMessage(e), "\n")}
      )
      
      event_i_final_url = paste0(event_i_info_url, "/Final")
      if(url.exists(event_i_final_url))
      {
        # download.file(event_i_final_url, "Marks Final.html")
        event_i_final_html = read_html(event_i_final_url)
        event_i_final_judges_identifiers = event_i_final_html %>% html_nodes(css = "#final .ajud") %>% html_text()
        event_i_final_dances = gsub("?<=[\\s])\\s*|^\\s+|\\s+$", "", (event_i_final_html %>% html_nodes(css = "#final .dance") %>% html_text()))
        event_i_final_dance_count = length(event_i_final_dances)
        event_i_final_couplenumbers = event_i_final_html %>% html_nodes(css = "#final .number") %>% html_text()
        event_i_final_marks_count = length(event_i_final_couplenumbers)
        event_i_final_couple_count = event_i_final_marks_count/event_i_final_dance_count
        event_i_final_judges_marks = vector(mode = "list")
        event_i_final_dance_places = event_i_final_html %>% html_nodes(css = "#final .rankTotal") %>% html_text()
        
        for(j in 1:length(event_i_final_judges_identifiers))
        {
          event_i_final_judges_marks[[j]] = event_i_final_html %>% html_nodes(css = paste0("#final .rank:nth-child(", j+1, ")")) %>% html_text()
          for(k in 1:event_i_final_marks_count)
          {
            final_ijk_event_id = event_id[i]
            final_ijk_round_name = "Final"
            final_ijk_couple_id = event_i_couple_id[which(event_i_final_couplenumbers[k] == event_i_couple_number)]
            final_ijk_judge_id = event_i_judges_id[which(event_i_final_judges_identifiers[j] == event_i_judges_identifier)]
            final_ijk_final_dance = event_i_final_dances[ceiling(k/event_i_final_couple_count)]
            final_ijk_mark_given = event_i_final_judges_marks[[j]][k]
            
            final_ijk = data.frame(event_id = final_ijk_event_id, round_name = final_ijk_round_name, couple_id = final_ijk_couple_id, judge_id = final_ijk_judge_id, final_dance = final_ijk_final_dance, final_mark_given = final_ijk_mark_given)
            if(nrow(MarksFinal) == 0)
            {
              MarksFinal = rbind(MarksFinal, final_ijk)
              write.csv(x = MarksFinal, file = "MarksFinal.csv", row.names = FALSE)
            } else  {
              write.table(x = final_ijk, file = "MarksFinal.csv", append = TRUE, sep = ",", row.names = FALSE, col.names = FALSE)
            }
          }
          #rm(final_ijk_event_id, final_ijk_round_name, final_ijk_couple_id, final_ijk_judge_id, final_ijk_final_dance, final_ijk_mark_given, final_ijk)
          gc()
        }
        for(j in 1:event_i_final_marks_count)
        {
          final_ij_event_id = event_id[i]
          final_ij_round_name = "Round"
          final_ij_couple_id = event_i_couple_id[which(event_i_final_couplenumbers[j] == event_i_couple_number)]
          final_ij_judge_id = "Cumulative"
          final_ij_final_dance = event_i_final_dances[ceiling(j/event_i_final_couple_count)]
          final_ij_mark_given = event_i_final_dance_places[j]
          
          final_ij = data.frame(event_id = final_ij_event_id, round_name = final_ij_round_name, couple_id = final_ij_couple_id, judge_id = final_ij_judge_id, final_dance = final_ij_final_dance, final_mark_given = final_ij_mark_given)
          write.table(x = final_ij, file = "MarksFinal.csv", append = TRUE, sep = ",", row.names = FALSE, col.names = FALSE)
          
          #rm(final_ij_event_id, final_ij_round_name, final_ij_couple_id, final_ij_judge_id, final_ij_final_dance, final_ij_mark_given)
          gc()
        }
        Sys.sleep(1)
      }
      cat("MarksFinal updated\n\n")
      #rm(event_i_rankings_html, event_i_couple_placement, event_i_event_id, event_i_couple_url, event_i_couple_country, event_i_couple_number, event_i_couple_id, event_i_placement, event_i_couple_id_new, event_i_couple_country_new, event_i_couple_joindate, event_i_couple_agegroup, event_i_couple_status, event_i_couple_division, event_i_couple_athlete_memberid_male, event_i_couple_athlete_memberid_female, event_i_couple, event_i_info_url, event_i_info_html, event_i_round_round_name, event_i_round_event_id, event_i_round_couples_count, event_i_round, event_i_judges_url, event_i_judges_html, event_i_judges_name, event_i_judges_id, event_i_judges_country, event_i_judges_identifier, event_i_marks_url, event_i_marks_html, event_i_marks_dances, event_i_marks_identifiers, event_i_marks_unique_identifiers, match_vector, event_i_marks_judges_id, event_i_marks_table, row_shift, numberof_dances, numberof_judges, col_names, idx_1, idx_2, pref, event_i_final_url, event_i_final_html, event_i_final_judges_identifiers, event_i_final_dances, event_i_final_dance_count, event_i_final_couplenumbers, event_i_final_marks_count, event_i_final_couple_count, event_i_final_judges_marks, event_i_final_dance_places)
      gc()
      
    }, error = function(e){cat("Error: ", conditionMessage(e), "\n\n")}
  )
}
stopCluster(cl)
