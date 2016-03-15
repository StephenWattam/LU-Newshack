#!/usr/bin/env ruby


CANDY_API_KEY = 'Bd1QARJ8BD2rAfE9i9igC8IlDR6ywXVG'
JUICER_API_KEY = 'Yk3KFzyVliTamletdhg7FOAqf26vwGeL'

CANDY_HEADERS = {
  'X-Candy-Platform' => 'Desktop',
  'X-Candy-Audience' => 'International',
  'Accept' => 'application/json'
}

CANDY_ENDPOINT = "http://content-api-a127.api.bbci.co.uk/asset/"
CATEGORIES = {:en => %w{news/world news/uk news/world/africa news/world/europe news/world/asia news/world/australia news/world/latin_america news/world/middle_east news/world/us_and_canada news/technology news/business sport/football},
              :ar => %w{arabic/sports arabic/middleeast arabic/worldnews arabic/business arabic/artandculture arabic/topics/magazine},
              :es => %w{mundo/temas/america_latina mundo/temas/internacional mundo/temas/economia mundo/temas/tecnologia mundo/temas/ciencia mundo/temas/salud mundo/temas/cultura mundo/temas/deportes},
              :zh => %w{zhongwen/simp/world zhongwen/simp/chinese_news zhongwen/simp/uk zhongwen/simp/indepth zhongwen/simp/science zhongwen/simp/business},
              :pt => %w{portuguese/topicos/brasil portuguese/topicos/internacional portuguese/topicos/economia portuguese/topicos/saude portuguese/topicos/ciencia_e_tecnologia portuguese/topicos/aprenda_ingles portuguese/topicos/salasocial}
}

require 'rest-client'
require 'json'


class Hash
  # Resurively search for something
  def find_key(key)
    accum = []

    self.keys.each do |k|
      accum << self[k] if k == key

      accum += self[k].find_key(key) if self[k].is_a?(Hash) || self[k].is_a?(Array)
    end

    return accum
  end
end

class Array
  # Resurively search for something
  def find_key(key)
    accum = []

    self.each do |a|
      accum += a.find_key(key) if a.is_a?(Hash)
    end

    accum
  end
end




stubs = {}
CATEGORIES.each do |language, cats|

  puts "\n==> LANG: #{language}"
  cats.each do |cat|

    puts "Category: #{cat}"

    endpoint = "#{CANDY_ENDPOINT}#{cat}?api_key=#{CANDY_API_KEY}"
    # warn "DEBUG: #{endpoint}"
    res = RestClient::Request.execute(method: :get,
                                         url: endpoint,
                                         headers: CANDY_HEADERS)

    res = JSON.parse(res)
    puts " #{res.length} results."

    
    stubs[language] ||= {}
    stubs[language][cat] ||= []
    (res['results'] || []).each do |r|
      stubs[language][cat] += r.find_key("assetUri")
    end

    puts "Total for #{language}, #{cat} => #{stubs[language][cat].length}"

  end

end




# Fetch pages
stubs.each do |lang, cats|
  puts "\n==> LANG: #{lang}"

  cats.each do |cat, sts|
    puts "Category: #{cat}"

    articles = {}
    sts.each_with_index do |stub, i|

      puts " #{i}/#{sts.length} #{stub}..."

      begin
        endpoint = "#{CANDY_ENDPOINT}#{stub}?api_key=#{CANDY_API_KEY}"
        # warn "DEBUG: #{endpoint}"
        res = RestClient::Request.execute(method: :get,
                                          url: endpoint,
                                          headers: CANDY_HEADERS)


        res = JSON.parse(res)
        article = res['results'].first
      rescue Exception
      end

      articles[stub] = article
    end

    stubs[lang][cat] = articles

  end
end


File.open("out.json", 'w') do |io|
  io.write(JSON.dump(stubs))
end


